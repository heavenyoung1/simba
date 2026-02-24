from dataclasses import dataclass

@dataclass
class ScalingRule:
    min_field: int
    max_field: int
    min_engineering: int
    max_engineering: int