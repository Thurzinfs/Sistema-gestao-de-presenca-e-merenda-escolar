from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ClassroomInDTO(BaseModel):
    school: UUID
    name: str


class ClassroomOutDTO(BaseModel):
    id: UUID
    school: UUID
    name: str
    active: bool
    created_at: datetime

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            school=model.school,
            name=model.name,
            active=model.active,
            created_at=model.created_at,
        )


class ClassroomUpdateDTO(BaseModel):
    name: Optional[str] = None


class StudentsInDTO(BaseModel):
    classroom: UUID
    name: str
    ra: str
    qr_code: str


class StudentsOutDTO(BaseModel):
    id: UUID
    classroom: UUID
    name: str
    ra: str
    qr_code: str
    active: bool
    created_at: datetime

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            classroom=model.classroom,
            name=model.name,
            ra=model.ra,
            qr_code=model.qr_code,
            active=model.active,
            created_at=model.created_at,
        )


class StudentsUpdateDTO(BaseModel):
    name: Optional[str] = None
    ra: Optional[str] = None
    qr_code: Optional[str] = None
