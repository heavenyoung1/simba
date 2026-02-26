from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterAddress:
    address: int
    bit_index: int | None

    @classmethod
    def from_modbus_string(
        cls,
        raw: str,
        bit_index: int | None = None,
    ) -> 'RegisterAddress':
        '''Парсит адрес вида 'MB4' → RegisterAddress(address=4, ...)'''
        return cls(address=int(raw[2:]), bit_index=bit_index)
