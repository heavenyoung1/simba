from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterAddress:
    address: int            
    bit_index: int | None