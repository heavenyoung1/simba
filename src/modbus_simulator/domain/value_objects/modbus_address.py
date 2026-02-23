from dataclasses import dataclass
from enum import Enum

class RegisterType(Enum):
    '''
    One of the four Modbus address space tables.

    Defines the register type and its access rules.
    '''
    COIL = 'coil'                  # DO  — read/write, 1 bit
    DISCRETE_INPUT = 'discrete'    # DI  — read only,  1 bit
    INPUT_REGISTER = 'input'       # AI  — read only,  16 bit
    HOLDING_REGISTER = 'holding'   # AO  — read/write, 16 bit

@dataclass(frozen=True)
class ModBusAddress:
    '''Unique coordinate of a single register in the Modbus address space.

    Identifies a register across three dimensions: table type, register number,
    and device address on the bus. Has no knowledge of the data type stored
    (int16, float32, etc.) — that is the responsibility of a higher-level object
    (e.g. Tag or RegisterDefinition).

    Value Object: immutable, compared by value, usable as a dictionary key.
    '''
    register_type: RegisterType
    address: int
    unit_id: int = 1

    def __post_init__(self):
        if not 0 <= self.address <= 65535:
            raise ValueError(f'Modbus address {self.address} out of range')