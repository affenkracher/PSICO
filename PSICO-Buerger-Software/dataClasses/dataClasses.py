from dataclasses import dataclass
from typing import List

@dataclass
class PingData:
    address: str
    allowed: bool
    frequency: int

@dataclass
class Failing:
    kind: str
    description: str
    frequency: int

@dataclass
class KeyData:
    key: str
    frequency: int

@dataclass
class MouseData:
    x: int
    y: int
    frequency: int

@dataclass
class Citizen:
    name: str
    keyInput: List[KeyData]
    incrimaterial: List[str]
    proof: List[str]
    pings: List[PingData]
    mouseInput: List[MouseData]
    failings: List[Failing]
    socialCreditScore: int