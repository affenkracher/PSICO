from dataclasses import dataclass
from typing import List

"""
AUTHOR: PHILIPP WENDEL
"""

"""
DataClasses are a quick and easy way to implement data-holding objects in Python,
with all the getter, setter, equal and __str__ methods auto-generated.
"""

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

"""
The Citizen DataClass holds the information about the machines assigned citizen.
It stores every logged input (Keyboard, Mouse, Tasks, ...) and allows quick and easy reference
in other modules
"""

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