from pymodbus.datastore import (
    ModbusDeviceContext,
    ModbusServerContext,
    ModbusSparseDataBlock,
)
from pymodbus.server import StartAsyncTcpServer

from application.register_assembler import RegisterAssembler
from domain.entities.analog import AnalogSignal
from domain.entities.discrete import DiscreteSignal


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

    async def start(
        self, 
        signals: list[AnalogSignal | DiscreteSignal],
        ) -> None:

        registers = self._load_registers(signals)
        self._context = self._make_context(registers)

        await StartAsyncTcpServer(
            address=(self.host, self.port),
            context=self._context
        )

    def _load_registers(
            self, 
            signals: list[AnalogSignal | DiscreteSignal],
            ):
        registers = self._assembler.build(signals)
        return registers

    def _make_context(
            self, 
            registers: dict[int, int],
            ) -> ModbusServerContext:
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