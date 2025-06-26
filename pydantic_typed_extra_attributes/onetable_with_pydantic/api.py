import dataclasses
from datetime import datetime


@dataclasses.dataclass
class IntegrationAData:
    start: datetime
    end: datetime
    name: str
    custom_prop_a: str

@dataclasses.dataclass
class IntegrationBData:
    start: datetime
    end: datetime
    name: str
    custom_prop_b: str
