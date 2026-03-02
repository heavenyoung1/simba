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

class FunctionCode(Enum):
    READ_COILS               = 0x01
    READ_DISCRETE_INPUTS     = 0x02
    READ_HOLDING_REGISTERS   = 0x03
    READ_INPUT_REGISTERS     = 0x04
    WRITE_SINGLE_COIL        = 0x05
    WRITE_SINGLE_REGISTER    = 0x06
    WRITE_MULTIPLE_COILS     = 0x0F
    WRITE_MULTIPLE_REGISTERS = 0x10