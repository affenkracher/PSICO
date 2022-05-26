from dataclasses import dataclass

@dataclass
class PingData:
    address: str
    allowed: bool
    frequency: int