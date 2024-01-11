import datetime
import asyncio
from .analyzer import (calculate_sdnn, calculate_rmssd, calculate_stress_score)
from bleak import BleakClient, BleakScanner
from .database import HeartRateDatabase, HeartRateTuple
import time

class HeartRateMonitor:
    def __init__(self, address, hr_measurement_char_uuid):
        self.address = address
        self.hr_measurement_char_uuid = hr_measurement_char_uuid
        self.event = asyncio.Event()
        self.ibi_value = 0 
        self.ibi_timestamp = 0
        self.hr_db = HeartRateDatabase('database.db')
        self.date = datetime.date.today()

    async def start_monitoring(self):
        while True:
            async with BleakScanner(self.scan_handler) as scanner:
                await self.event.wait()
                self.event.clear()
                self.date = datetime.date.today()
                if datetime.datetime.now().time() > datetime.time(17, 00, 00):
                    self.date = self.date + datetime.timedelta(days=1)
                client = BleakClient(self.address, disconnected_callback=self.disconnect_handler, timeout=30)
                await scanner.stop()
                try:
                    if not client.is_connected:
                        await client.connect()
                    print("Connected to device with address:", self.address, datetime.datetime.now())
                    await client.start_notify(self.hr_measurement_char_uuid, self.handle_rr_intervals)
                    await self.event.wait()
                    self.event.clear()
                except Exception as e:
                    print(e)
                finally:
                    await client.disconnect()
                self.ibi_value = 0
                time.sleep(60)
                

    def scan_handler(self, device, _):
        if device.address == self.address:
            self.event.set()

    def disconnect_handler(self, _):
        self.event.set()
        print("Disonnected from device with address:", self.address, datetime.datetime.now())
        return

    def handle_rr_intervals(self, _, data):
        print(data[1])
        interval = int(60000 / data[1])
        current_timestamp = int(datetime.datetime.now().timestamp())
        if self.ibi_value != 0:
            rmssd = calculate_rmssd([self.ibi_value, interval])
            sdnn = calculate_sdnn([self.ibi_value, interval])
            stress_score = calculate_stress_score(data[1], rmssd, sdnn)
            data = HeartRateTuple(data[1], interval, rmssd, sdnn, stress_score, current_timestamp, self.date)
            self.hr_db.insert(data)
        self.ibi_value = interval
