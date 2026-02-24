from dataclasses import dataclass

@dataclass(frozen=True)
class ScalingRule:
    min_eu: float    # EU = Engineering Units, инженерные единицы
    max_eu: float    # например 4.0 — 20.0 мА
    min_raw: float   # raw = сырое значение в регистре
    max_raw: float   # например 4000.0 — 20000.0

    def scale(self, eu_value: float) -> float:
        result = (self.max_raw - self.min_raw)
            