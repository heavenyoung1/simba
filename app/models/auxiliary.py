from enum import Enum

class SignalType(str, Enum):
    AI = "AI"
    AO = "AO"
    DI = "DI"
    DO = "DO"

class Direction(str, Enum):
    READING = "READING"
    WRITING = "WRITING"

class DataType(str, Enum):
    USHORT = "USHORT"
    SHORT = "SHORT"
    BOOL = "BOOL"
    UINT = "UINT"
    INT = "INT"

class ModbusFunction(Enum):
    COIL                = "0x"
    DISCRETE_INPUT      = "1x"
    INPUT_REGISTER      = "3x"
    HOLDING_REGISTER    = "4x"

    @classmethod
    def find_method(cls, raw: str) -> "ModbusFunction":
        prefix = raw[:2].lower()
        try:
            return cls(prefix)
        except ValueError:
            raise ValueError(f"Unknown prefix in address: {raw!r}")