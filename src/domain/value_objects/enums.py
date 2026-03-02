from enum import Enum


class Direction(Enum):
    WRITING = 'WRITING'
    READING = 'READING'


class DataType(Enum):
    USHORT = 'USHORT'
    BOOLEAN = 'BOOLEAN'


class Driver(Enum):
    MBTCP = 'MBTCP'


class XMLHeadObjects(Enum):
    ANALOGS = 'AnalogOutputs'
    DISCRETES = 'DiscreteInputs'


class XMLObjects(Enum):
    AI = 'Analog'
    DI = 'Discrete'

class ModbusFunction(Enum):
    COIL                = '0x'
    DISCRETE_INPUT      = '1x'
    INPUT_REGISTER      = '3x'
    HOLDING_REGISTER    = '4x'

    @classmethod
    def find_method(cls, raw: str) -> 'ModbusFunction':
        prefix = raw[:2].lower()
        try:
            return cls(prefix)
        except ValueError:
            raise ValueError(f'Неизвестный префикс в адресе: {raw!r}')