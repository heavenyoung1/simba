from dataclasses import dataclass

from src.domain.value_objects.modbus_address import RegisterAddress
from src.domain.value_objects.enums import Driver, DataType, Direction


@dataclass
class DiscreteSignal:
    direction: Direction
    tag: str
    name: str
    address: RegisterAddress
    inversed: bool
    driver: Driver

    forced: bool
    forced_value: bool

    current_value: bool = False