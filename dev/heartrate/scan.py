import asyncio
from bleak import BleakScanner

async def scan_for_devices():
    dev = []
    def callback(device, advertisement_data):
        dev.append(device.address)
        print(f"{len(dev)}. Device {device} (advertisement data: {advertisement_data})")
    scanner = BleakScanner(callback)
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()
    print("Choose device to connect to:")
    choosen_device = int(input()) 
    # print dev to file
    with open("hr-sensor.txt", "w") as f:
        f.write(dev[choosen_device-1])
    

asyncio.run(scan_for_devices())
