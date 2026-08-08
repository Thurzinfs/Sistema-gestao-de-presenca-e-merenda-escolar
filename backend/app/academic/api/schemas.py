from datetime import datetime
from os import name
from typing import Optional
from uuid import UUID
from ninja import Schema

from app.academic.application.dtos import (
    ClassroomInDTO,
    ClassroomUpdateDTO,
    StudentsInDTO,
    StudentsUpdateDTO,
)


class ClassroomIn(Schema):
    school: UUID
    name: str

    def to_dto(self) -> ClassroomInDTO:
        return ClassroomInDTO(school=self.school, name=self.name)


class ClassroomOut(Schema):
    id: UUID
    school: UUID
    name: str
    active: bool
    created_at: datetime

    @staticmethod
    def from_domain(dto):
        return ClassroomOut(
            id=dto.id,
            school=dto.school,
            name=dto.name,
            active=dto.active,
            created_at=dto.created_at,
        )


class ClassroomUpdate(Schema):
    name: Optional[str] = None

    def to_dto(self) -> ClassroomUpdateDTO:
        return ClassroomUpdateDTO(name=self.name)


class StudentsIn(Schema):
    classroom: UUID
    name: str
    ra: str
    qr_code: str

    def to_dto(self) -> StudentsInDTO:
        return StudentsInDTO(
            classroom=self.classroom,
            name=self.name,
            ra=self.ra,
            qr_code=self.qr_code,
        )


class StudentsOut(Schema):
    id: UUID
    classroom: UUID
    name: str
    ra: str
    active: bool
    qr_code: str
    created_at: datetime

    @staticmethod
    def from_domain(dto):
        return StudentsOut(
            id=dto.id,
            classroom=dto.classroom,
            name=dto.name,
            ra=dto.ra,
            qr_code=dto.qr_code,
            active=dto.active,
            created_at=dto.created_at,
        )


class StudentsUpdate(Schema):
    name: Optional[str] = None
    ra: Optional[str] = None
    qr_code: Optional[str] = None

    def to_dto(self) -> StudentsUpdateDTO:
        return StudentsUpdateDTO(
            name=self.name, ra=self.ra, qr_code=self.qr_code
        )
