from dataclasses import dataclass,field
from datetime import datetime, date as Date
from uuid import UUID,uuid4

from app.presence.domain.role import MomentRole, SnackRole

@dataclass
class ReadingEntity:
    id: UUID = field(default_factory=uuid4)
    student: UUID | None = field(default=None)
    moment: MomentRole | str = field(default=MomentRole.snack_afternoon)
    date_time: datetime = field(default_factory=datetime.now)

@dataclass
class FrequencyEntity:
    id: UUID = field(default_factory=uuid4)
    student: UUID | None = field(default=None)
    date: Date = field(default_factory=datetime.now)
    on_time: bool = field(default=False)
    reading: UUID | None = field(default=None)

@dataclass
class RegisterSnackEntity:
    id: UUID = field(default_factory=uuid4)
    student: UUID | None = field(default=None)
    date: Date = field(default_factory=datetime.now)
    moment: MomentRole | str = field(default=MomentRole.snack_afternoon)
    type_snack: SnackRole | str = field(default=SnackRole.normal)
    reading: UUID | None = field(default=None)