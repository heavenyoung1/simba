from pymodbus.datastore import (
    ModbusDeviceContext,
    ModbusServerContext,
    ModbusSparseDataBlock,
)
from pymodbus.server import StartAsyncTcpServer, StartTcpServer

from src.application.logger import logger
from src.application.register_assembler import RegisterAssembler
from src.domain.entities.analog import AnalogSignal
from src.domain.entities.discrete import DiscreteSignal

_SLAVE_ID = 0x00
_FC_HOLDING_REGISTERS = 3


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

    def _make_context(self, registers: dict[int, int]) -> ModbusServerContext:
        block = ModbusSparseDataBlock(registers) if registers else ModbusSparseDataBlock({0: 0})
        zero_block = ModbusSparseDataBlock({0: 0})

        device = ModbusDeviceContext(
            di=zero_block,
            co=zero_block,
            hr=block,
            ir=zero_block,
        )
        return ModbusServerContext(devices=device, single=True)

    def init(self, signals: list[AnalogSignal | DiscreteSignal]) -> None:
        """Собрать регистры из сигналов и инициализировать контекст сервера."""
        registers = self._assembler.build(signals)
        self._context = self._make_context(registers)
        logger.info('Modbus context initialized with %d registers', len(registers))

    def update(self, signals: list[AnalogSignal | DiscreteSignal]) -> None:
        """Обновить значения holding-регистров без перезапуска сервера."""
        if self._context is None:
            raise RuntimeError('ModbusServer not initialized. Call init() first.')

        registers = self._assembler.build(signals)
        device = self._context[_SLAVE_ID]

        for address, value in registers.items():
            device.setValues(_FC_HOLDING_REGISTERS, address, [value])

        logger.debug('Updated %d holding registers', len(registers))

    async def serve_async(self, signals: list[AnalogSignal | DiscreteSignal]) -> None:
        """Запустить сервер в асинхронном режиме (корутина блокируется до отмены)."""
        self.init(signals)
        logger.info('Starting Modbus TCP server on %s:%d', self.host, self.port)
        await StartAsyncTcpServer(
            context=self._context,
            address=(self.host, self.port),
        )

    def serve(self, signals: list[AnalogSignal | DiscreteSignal]) -> None:
        """Запустить сервер в синхронном (блокирующем) режиме."""
        self.init(signals)
        logger.info('Starting Modbus TCP server on %s:%d', self.host, self.port)
        StartTcpServer(
            context=self._context,
            address=(self.host, self.port),
        )