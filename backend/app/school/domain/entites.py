from dataclasses import dataclass, field
from datetime import datetime, time
from uuid import UUID, uuid4

from pydantic import EmailStr

from app.school.domain.exceptions import ConflictFieldException
from app.school.domain.role import ManagerRole
from app.school.domain.value_objects import SchoolTimeVO


@dataclass
class SchoolEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    time_closing_presence: SchoolTimeVO | None = field(default=None)
    time_send_lunch: SchoolTimeVO | None = field(default=None)
    time_send_snack_afternoon: SchoolTimeVO | None = field(default=None)
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

        self.time_closing_presence = SchoolTimeVO(time)

    def change_time_send_lunch(self, time: time):
        if not time:
            raise ConflictFieldException('required new time')

        self.time_send_lunch = SchoolTimeVO(time)

    def change_time_snack_afternoon(self, time: time):
        if not time:
            raise ConflictFieldException('required new time')

        self.time_send_snack_afternoon = SchoolTimeVO(time)

    def change_number_whats(self, new_number: str):
        if not new_number:
            raise ConflictFieldException('required new_number')

        self.number_whats = new_number


@dataclass
class ManagerEntity:
    id: UUID = field(default_factory=uuid4)
    school: UUID | None = field(default=None)
    role: ManagerRole | str = field(default=ManagerRole.pending)
    name: str = field(default='')
    email: EmailStr | str = field(default='')
    password: str = field(default='')
    active: bool = field(default=True)
    created_at: datetime = field(default_factory=datetime.now)

    def deactive(self):
        if self.active == False:
            raise ConflictFieldException('manager already deactivate')

        self.active = False

    def change_role(self, new_role: str):
        if not new_role:
            raise ConflictFieldException('required new role')

        self.role = new_role

    def change_name(self, new_name: str):
        if not new_name:
            raise ConflictFieldException('required new name')

        self.name = new_name

    def change_email(self, new_email: EmailStr):
        if not new_email:
            raise ConflictFieldException('required new email')

        self.email = new_email

    def change_password(self, new_password: str):
        if not new_password:
            raise ConflictFieldException('required new password')

        self.password = new_password
