from dataclasses import dataclass

from src.domain.value_objects.modbus_address import RegisterAddress
from src.domain.value_objects.scaling import ScalingRule
from src.domain.value_objects.enums import Driver, DataType, Direction


@dataclass
class AnalogSignal:
    '''
    Аналоговый сигнал (AI/AO).

    Атрибуты:
        direction       -- направление сигнала: READING (чтение с устройства) или WRITING (запись на устройство)
        tag             -- уникальный идентификатор сигнала в системе (напр. "PT-101")
        name            -- читаемое имя / описание (напр. "Давление на входе")
        data_type       -- тип сырых данных в регистре Modbus (USHORT, BOOLEAN и т.д.)
        address         -- адрес регистра Modbus (содержит префикс функции и номер)
        driver          -- протокол опроса (MBTCP — Modbus TCP)
        scaling         -- правило масштабирования raw → EU; None если масштабирование не задано
        scaling_enabled -- True = масштабирование активно, False = значение передаётся без пересчёта

        forced          -- True = сигнал принудительно подменён (override активен)
        forced_input    -- определяет единицу forced_value:
                              False = значение задано в raw (сырых единицах регистра),
                              True  = значение задано в EU (инженерных единицах)
        forced_value    -- подменённое значение; интерпретация зависит от forced_input

        current_value_eu -- текущее актуальное значение в инженерных единицах (EU)
    '''

    direction: Direction
    tag: str
    name: str
    data_type: DataType
    address: RegisterAddress
    driver: Driver
    scaling: ScalingRule | None
    scaling_enabled: bool

    forced: bool
    forced_input: bool  # False = raw (сырые единицы), True = EU (инженерные единицы)
    forced_value: float  # подменённое значение; интерпретация зависит от forced_input

    current_value_eu: float = 0.0
