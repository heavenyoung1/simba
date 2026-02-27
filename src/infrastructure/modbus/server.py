from pymodbus.datastore import (
    ModbusDeviceContext,
    ModbusServerContext,
    ModbusSparseDataBlock,
)


from pymodbus.server import StartAsyncTcpServer, StartTcpServer

from domain.entities.analog import AnalogSignal
from domain.entities.discrete import DiscreteSignal

from application.register_assembler import RegisterAssembler


class ModbusServer:
    def __init__(
            self,
            host: str = '0.0.0.0',
            port: int = 502,

    ) -> None:
        self.host = host
        self.port = port
        self._context: ModbusServerContext | None = None
        self._assembler = RegisterAssembler()

    async def start(self) -> None:
        await StartAsyncTcpServer(
            address=(self.host, self.port),
        )

    async def _loag_registers(self, signals: list[AnalogSignal | DiscreteSignal]):
        registers = self._assembler.build(signals)

    def _make_context(self, registers: dict[int, int]) -> ModbusServerContext:
        block = ModbusSparseDataBlock(registers)
        zero_block = ModbusSparseDataBlock({0: 0})

        device = ModbusDeviceContext(
            di=zero_block,
            co=zero_block,
            hr=block,
            ir=zero_block,
        )
        return ModbusServerContext(
            devices=device,
            single=True
        )