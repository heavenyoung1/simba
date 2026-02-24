from dataclasses import dataclass

from src.domain.value_objects.modbus_address import RegisterAddress
from src.domain.value_objects.scaling import ScalingRule
from domain.value_objects.enums import Driver, DataType, Direction

@dataclass
class AnalogSignal:
    direction: Direction
    tag: str
    name: str
    data_type: DataType
    address: RegisterAddress
    driver: Driver
    scaling: ScalingRule | None
    scaling_enabled: bool

    forced: bool        # форсирование вообще включено?
    forced_input: bool  # True = используем forced_eu, False = используем forced_raw
    forced_raw: float   # Сырое значением имитируем (либо одно)
    forced_eu: float    # Инженерное значение имитируем (либо другое)


