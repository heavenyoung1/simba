from auxiliary import (
    DataType,
    Direction,
    SignalType,
    ModbusFunction,
)

from dataclasses import dataclass
from typing import Optional

@dataclass
class BaseSignal:
    """Abstract base for all signal types."""
    tag: str
    name: str
    address: int            # 0-based Modbus address
    register_type: ModbusFunction
    data_type: DataType
    direction: Direction
    forced: bool
    forced_value: Optional[float]
    current_raw_value: int = 0
    enabled: bool = True
 
    @property
    def signal_type(self) -> SignalType:
        raise NotImplementedError
    

@dataclass
class AnalogSignal(BaseSignal):
    """AI/AO signal with optional linear scaling."""
    scaling: bool = False
    min_input: float = 0.0
    max_input: float = 100.0
    min_output: float = 0.0
    max_output: float = 65535.0
    force_input: bool = False

    @property
    def signal_type(self) -> SignalType:
        return SignalType.AI
    
    #TODO Create method for converting engineer unit and raw
    
@dataclass
class DigitalSignal(BaseSignal):
    """DI/DO signal — single bit."""
 
    @property
    def signal_type(self) -> SignalType:
        return SignalType.DIGITAL
 
    @property
    def bool_value(self) -> bool:
        return bool(self.current_raw_value)
