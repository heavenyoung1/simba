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