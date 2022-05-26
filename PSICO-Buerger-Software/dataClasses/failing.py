from dataclasses import dataclass

@dataclass
class Failing:
    kind: str
    description: str
    frequency: int