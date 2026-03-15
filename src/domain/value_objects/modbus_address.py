from dataclasses import dataclass

from src.domain.value_objects.enums import ModbusFunction

@dataclass(frozen=True)
class RegisterAddress:
    function: ModbusFunction
    address: int
    bit_index: int | None

    @classmethod
    def from_modbus_string(
        cls,
        raw: str,
        bit_index: int | None = None,
    ) -> 'RegisterAddress':
        '''Парсит адрес вида 'MB4' → RegisterAddress(address=4, ...)'''
        return cls(
            function=ModbusFunction.find_method(raw),
            address=int(raw[2:]), 
            bit_index=bit_index,
            )