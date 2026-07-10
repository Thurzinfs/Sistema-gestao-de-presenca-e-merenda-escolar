from dataclasses import dataclass, field
from datetime import datetime, time
from uuid import UUID, uuid4

from pydantic import EmailStr

from app.school.domain.exceptions import ConflictFieldException
from app.school.domain.role import ManagerRole


@dataclass
class SchoolEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    time_closing_presence: time | None = field(default=None)
    time_send_lunch: time | None = field(default=None)
    time_send_snack_afternoon: time | None = field(default=None)
    number_whats: str | None = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def deactive(self):
        if self.deleted_at is not None:
            raise ConflictFieldException('school already deactivate')

        self.deleted_at = datetime.now()
    
