from dataclasses import dataclass,field
from datetime import datetime
from uuid import UUID,uuid4

from app.presence.domain.role import MomentRole, SnackRole

@dataclass
class ReadingEntity:
    id: UUID = field(default_factory=uuid4)
    student_id: UUID | None = field(default=None)
    moment: MomentRole | None = field(default=MomentRole.snack_afternoon)
    date_time: datetime = field(default_factory=datetime.now)

@dataclass
class FrequencyEntity:
    id: UUID = field(default_factory=uuid4)
    student_id: UUID | None = field(default=None)
    date: datetime = field(default_factory=datetime.now)
    on_time: bool = field(default=False)
    reading_id: UUID | None = field(default=None)

@dataclass
class RegisterSnackEntity:
    id: UUID = field(default_factory=uuid4)
    student_id: UUID | None = field(default=None)
    date: datetime = field(default_factory=datetime.now)
    moment: MomentRole | None = field(default=MomentRole.snack_afternoon)
    type_snack: SnackRole | None = field(default=SnackRole.normal)
    reading_id: UUID | None = field(default=None)