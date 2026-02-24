from dataclasses import dataclass
from enum import Enum

@dataclass
class RegisterAddress:
    address: str            # Например 4x37069
    bit_index: int | None   # Для дискрета будет индекс бита, для аналога None