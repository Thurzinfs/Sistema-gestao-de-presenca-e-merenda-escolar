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
    
    def change_name(self, new_name: str):
        if not new_name:
            raise ConflictFieldException('required new name')
        
        self.name = new_name

    def change_time_closing_presence(self, time: time):
        if not time:
            raise ConflictFieldException('required new time')
        
        self.time_closing_presence = time

    def change_time_send_lunch(self, time: time):
        if not time:
            raise ConflictFieldException('required new time')
        
        self.time_send_lunch = time

    def change_time_snack_afternoon(self, time: time):
        if not time:
            raise ConflictFieldException('required new time')
        
        self.time_send_snack_afternoon = time


@dataclass
class ManagerEntity:
    id: UUID = field(default_factory=uuid4)
    school_id: UUID | None = field(default=None)
    role: ManagerRole | str = field(default=ManagerRole.pending)
    name: str = field(default='')
    email: EmailStr | str = field(default='')
    password: str = field(default='')
    active: bool = field(default=True)
    created_at: datetime = field(default_factory=datetime.now)

    def deactive(self):
        if self.active == False:
            raise ConflictFieldException('manager already deactivate')

        self.active = True
    