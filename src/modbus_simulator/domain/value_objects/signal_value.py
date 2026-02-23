from dataclasses import dataclass

@dataclass(frozen=True)
class ScaleConfig:
    '''
    Настройки масштабирования аналогового сигнала.

    Описывает линейное преобразование между сырым значением регистра Modbus
    и инженерными единицами измерения.

    Пример: давление насоса
        raw_min=4000,  raw_max=20000  — диапазон АЦП (4–20 мА)
        min_value=0.0, max_value=6.0  — диапазон в МПа
    '''
    min_value: float        # инженерное значение при raw_min
    max_value: float        # инженерное значение при raw_max
    raw_min: int = 4000     # полевое значение при минимуме (4 мА)
    raw_max: int = 20000    # полевое значение при максимуме (20 мА)
    unit: str = ''          # единица измерения: 'МПа', '°C', 'м³/ч'

    def __post_init__(self):
        if self.min_value >= self.max_value:
            raise ValueError(
                f'min_value ({self.min_value}) должен быть меньше '
                f'max_value ({self.max_value})'
            )
        if self.raw_min >= self.raw_max:
            raise ValueError(
                f'raw_min ({self.raw_min}) должен быть меньше '
                f'raw_max ({self.raw_max})'
            )
        
@dataclass(frozen=True)
class SignalValue:
    '''
    Неизменяемый контейнер значения сигнала.

    Хранит одновременно сырое значение из регистра Modbus и
    инженерное значение в реальных единицах измерения.

    Для дискретных сигналов (DI/DO): raw = 0 или 1, engineering = bool
    Для аналоговых сигналов (AI/AO): raw = 4000..20000, engineering = float
    '''
    raw: int                    # полевое значение из регистра Modbus (мА)
    engineering: float | bool   # значение в инженерных единицах, например (МПа)
    unit: str = ''              # единица измерения

    @classmethod
    def from_discrete(cls, value: bool) -> 'SignalValue':
        '''Создать значение дискретного сигнала (DI/DO).'''
        return cls(
            raw=int(value),
            engineering=value,
        )
    
    @classmethod
    def from_raw_analog(cls, raw: int, scale: ScaleConfig | None) -> 'SignalValue':
        '''
        Создать значение аналогового сигнала из сырого значения регистра.

        Применяется при чтении AI — пересчитывает 4000..20000 в инженерные единицы.
        Если scale не задан — engineering равен raw.
        '''
        if scale is None:
            return cls(
                raw=raw,
                engineering=float(raw),
            )

        engineering = (
            scale.min_value
            + (raw - scale.raw_min)
            / (scale.raw_max - scale.raw_min)
            * (scale.max_value - scale.min_value)
        )
        return cls(raw=raw, engineering=round(engineering, 3), unit=scale.unit)
    
    @classmethod
    def from_engineering(cls, value: float, scale: ScaleConfig) -> 'SignalValue':
        '''
        Создать значение аналогового сигнала из инженерного значения.

        Применяется при записи AO — пересчитывает инженерные единицы в 4000..20000.
        '''
        raw = int(
            scale.raw_min
            + (value - scale.min_value)
            / (scale.max_value - scale.min_value)
            * (scale.raw_max - scale.raw_min)
        )
        # ограничиваем допустимым диапазоном
        raw = max(scale.raw_min, min(scale.raw_max, raw))
        return cls(raw=raw, engineering=value, unit=scale.unit)