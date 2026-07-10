from datetime import datetime, time
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr

from app.school.application.dtos import (
    ManagerInDTO,
    ManagerInUpdateDTO,
    ManagerOutDTO,
    SchoolInDTO,
    SchoolInUpdateDTO,
    SchoolOutDTO,
)
from app.school.domain.role import ManagerRole


class SchoolIn(Schema):
    name: str
    time_closing_presence: time
    time_send_lunch: time
    time_send_snack_afternoon: time
    number_whats: str

    def to_dto(self) -> SchoolInDTO:
        return SchoolInDTO(
            name=self.name,
            time_closing_presence=self.time_closing_presence,
            time_send_lunch=self.time_send_lunch,
            time_send_snack_afternoon=self.time_send_snack_afternoon,
            number_whats=self.number_whats,
        )


class SchoolOut(Schema):
    id: UUID
    name: str
    time_closing_presence: time
    time_send_lunch: time
    time_send_snack_afternoon: time
    number_whats: str
    created_at: datetime
    deleted_at: datetime

    @staticmethod
    def from_domain(dto: SchoolOutDTO):
        return SchoolOut(
            id=dto.id,
            name=dto.name,
            time_closing_presence=dto.time_closing_presence,
            time_send_lunch=dto.time_send_lunch,
            time_send_snack_afternoon=dto.time_send_snack_afternoon,
            number_whats=dto.number_whats,
            created_at=dto.created_at,
            deleted_at=dto.deleted_at,
        )


class SchoolUpdate(Schema):
    name: Optional[str] = None
    time_closing_presence: Optional[time] = None
    time_send_lunch: Optional[time] = None
    time_send_snack_afternoon: Optional[time] = None
    number_whats: Optional[str] = None

    def to_dto(self) -> SchoolInUpdateDTO:
        return SchoolInUpdateDTO(
            name=self.name,
            time_closing_presence=self.time_closing_presence,
            time_send_lunch=self.time_send_lunch,
            time_send_snack_afternoon=self.time_send_snack_afternoon,
            number_whats=self.number_whats,
        )


class ManagerIn(Schema):
    school_id: UUID
    role: ManagerRole | str
    name: str
    email: EmailStr | str
    password: str

    def to_dto(self) -> ManagerInDTO:
        return ManagerInDTO(
            school_id=self.school_id,
            role=self.role,
            name=self.name,
            email=self.email,
            password=self.password,
        )


class ManagerOut(Schema):
    id: UUID
    school_id: UUID
    role: ManagerRole | str
    name: str
    email: EmailStr | str
    password: str
    active: bool
    created_at: datetime

    @staticmethod
    def from_domain(dto: ManagerOutDTO):
        return ManagerOut(
            id=dto.id,
            school_id=dto.school_id,
            role=dto.role,
            name=dto.name,
            email=dto.email,
            password=dto.password,
            active=dto.active,
            created_at=dto.created_at,
        )
