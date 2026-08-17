from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class SchoolTimeVO:
    value: time

    def __post_init__(self):
        object.__setattr__(self, 'value', self.value.replace(tzinfo=None))

    def __str__(self) -> str:
        return self.value.strftime('%H:%M:%S')
