import asyncio

from src.infrastructure.modbus.client import ModbusClient


async def main():
    async with ModbusClient(host='192.168.201.1') as client:
        result = await client.read_holding_registers(address=1000, count=100)
        print(result)

asyncio.run(main())