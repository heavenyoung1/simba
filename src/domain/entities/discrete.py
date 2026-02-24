from dataclasses import dataclass

from src.domain.value_objects.modbus_address import RegisterAddress
from domain.value_objects.general import Driver, DataType, Direction

@dataclass
class DiscreteSignal:
    direction: Direction
    tag_name: str
    name: str
    data_type: DataType
    address: RegisterAddress
    inversed: bool
    driver: Driver
