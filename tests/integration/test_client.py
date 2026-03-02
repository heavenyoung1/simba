import asyncio

from src.infrastructure.modbus.client import ModbusClient


async def main():
    async with ModbusClient(host='192.168.201.81') as client:
        result = await client.read_holding_registers(address=2200, count=100)
        print(result)

        await client.write_registers(registers={2207: 4095})
        result_1 = await client.read_holding_registers(address=2200, count=100)
        print(result_1)


asyncio.run(main())