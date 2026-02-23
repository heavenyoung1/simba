from dataclasses import dataclass

@dataclass(frozen=True)
class SignalValue:
    '''
    Универсальный контейнер значения.
    Для DI/DO — bool, для AI/AO — float с инженерными единицами.
    '''
    raw: int                        # Что реально в регистре
    engineering: float | bool       # Что видит оператор (после scale)
    unit: str = ''                  # 'бар', '°C', 'м³/ч'

    @classmethod
    def from_raw(cls, raw: int, scale: 'ScaleConfig | None') -> 'SignalValue':
        if scale is None:
            return cls(raw=raw, engineering=bool(raw))
        eng = scale.min + (raw / 65535) * (scale.max - scale.min)
        return cls(raw=raw, engineering=round(eng, 3), unit=scale.unit)