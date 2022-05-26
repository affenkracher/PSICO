from dataclasses import dataclass
from typing import List

from keyboardData import KeyboardData
from mouseData import MouseData
from pingData import PingData
from failing import Failing

@dataclass
class Citizen:
    name: str
    keyInput: List[KeyboardData]
    incrimaterial: List[str]
    proof: List[str]
    pings: List[PingData]
    mouseInput: List[MouseData]
    failings: List[Failing]
    socialCreditScore: int