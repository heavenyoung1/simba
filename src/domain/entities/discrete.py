from dataclasses import dataclass

from src.domain.value_objects.modbus_address import RegisterAddress
from src.domain.value_objects.enums import Driver, DataType, Direction


@dataclass
class DiscreteSignal:
    '''
    Дискретный сигнал (DI/DO).

    Атрибуты:
        direction     -- направление сигнала: READING (чтение с устройства) или WRITING (запись на устройство)
        tag           -- уникальный идентификатор сигнала в системе (напр. "XV-101")
        name          -- читаемое имя / описание (напр. "Клапан подачи")
        address       -- адрес регистра Modbus (содержит префикс функции и номер)
        inversed      -- True = логика инвертирована (0 в регистре → True в системе, и наоборот)
        driver        -- протокол опроса (MBTCP — Modbus TCP)

        forced        -- True = сигнал принудительно подменён (override активен)
        forced_value  -- подменённое значение (True/False); активно только при forced = True

        current_value -- текущее актуальное значение сигнала после применения инверсии и форсирования
    '''

    direction: Direction
    tag: str
    name: str
    address: RegisterAddress
    inversed: bool
    driver: Driver

    forced: bool
    forced_value: bool  # подменённое значение; активно только при forced = True

    current_value: bool = False