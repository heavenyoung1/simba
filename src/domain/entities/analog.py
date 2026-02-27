from dataclasses import dataclass

from src.domain.value_objects.modbus_address import RegisterAddress
from src.domain.value_objects.scaling import ScalingRule
from src.domain.value_objects.enums import Driver, DataType, Direction


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

    forced: bool
    forced_input: bool  # False = raw, True = EU
    forced_value: float  # одно значение, интерпретация зависит от forced_input

    current_value_eu: float = 0.0
