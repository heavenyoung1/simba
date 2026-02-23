from dataclasses import dataclass
from enum import Enum

class RegisterType(Enum):
    '''
    Одна из четырёх таблиц адресного пространства Modbus.

    Определяет тип регистра и правила доступа к нему.
    '''
    COIL = 'coil'                  # DO  — read/write, 1 bit
    DISCRETE_INPUT = 'discrete'    # DI  — read only,  1 bit
    INPUT_REGISTER = 'input'       # AI  — read only,  16 bit
    HOLDING_REGISTER = 'holding'   # AO  — read/write, 16 bit

@dataclass(frozen=True)
class ModBusAddress:
    '''Уникальная координата одного регистра в адресном пространстве Modbus.

    Идентифицирует регистр по трём измерениям: тип таблицы, номер регистра
    и адрес устройства на шине. Не знает ничего о типе хранимых данных
    (int16, float32 и т.д.) — это ответственность вышестоящего объекта
    (например, Tag или RegisterDefinition).

    Value Object: иммутабелен, сравнивается по значению, пригоден как ключ словаря.
    '''
    register_type: RegisterType
    address: int
    unit_id: int = 1

    def __post_init__(self):
        if not 0 <= self.address <= 65535:
            raise ValueError(f'Modbus address {self.address} out of range')