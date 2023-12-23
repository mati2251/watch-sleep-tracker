import asyncio
from bleak import discover

async def scan_for_devices():
    devices = await discover()
    for d in devices:
        print(f"Device: {d.name}, Address: {d.address}, RSSI: {d.rssi}")

asyncio.run(scan_for_devices())
