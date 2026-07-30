from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.academic.domain.exceptions import ConflictFieldException

@dataclass
class ClassroomEntity:
    id: UUID = field(default_factory=uuid4)
    school: UUID | None = field(default=None)
    name: str = field(default='')
    active: bool = field(default=True)
    created_at: datetime = field(default_factory=datetime.now)

    def change_name(self, new_name: str):
        if not new_name:
            raise ConflictFieldException('required new name')
        self.name = new_name

    def deactivate(self):
        if not self.active:
            raise ConflictFieldException('Classroom already deactivate')
        self.active = False

@dataclass
class StudentsEntity:
    id: UUID = field(default_factory=uuid4)
    classroom: UUID | None = field(default=None)
    name: str = field(default='')
    ra: str = field(default='')
    active: bool = field(default=True)
    qr_code: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)

    def change_name(self, new_name: str):
        if not new_name:
            raise ConflictFieldException('required new name')
        self.name = new_name

    def change_ra(self, new_ra: str):
        if not new_ra:
            raise ConflictFieldException('required new RA')
        self.ra = new_ra

    def change_qr_code(self, new_qrcode: str):
        if not new_qrcode:
            raise ConflictFieldException('required new QRcode')
        self.qr_code = new_qrcode

    def deactive(self):
        if not self.active:
            raise ConflictFieldException('Students already deactivate')
        self.active = False