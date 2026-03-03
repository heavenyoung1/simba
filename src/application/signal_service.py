from src.application.register_assembler import RegisterAssembler

from src.domain.entities.analog import AnalogSignal
from src.domain.entities.discrete import DiscreteSignal

from src.infrastructure.modbus.client import ModbusClient


class SignalService:
    def __init__(
        self,
        signals: list[AnalogSignal, DiscreteSignal],
        client: ModbusClient,
        assembler: RegisterAssembler
    ):
        pass

    async def start(self):
        ...

    def stop(self):
        ...

    async def _run_cycle(self):
        ...