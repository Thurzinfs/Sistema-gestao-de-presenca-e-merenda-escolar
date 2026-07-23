from uuid import UUID
from typing import Optional
from datetime import datetime, date as Date
from pydantic import BaseModel


class DailyMenuInDTO(BaseModel):
    school: UUID
    date: Date
    main_course: str
    manager: UUID


class DailyMenuOutDTO(BaseModel):
    id: UUID
    school: UUID
    date: Date
    main_course: str
    manager: UUID
    created_at: datetime

    @classmethod
    def from_domain(cls, entity):
        return cls(
            id=entity.id,
            school=entity.school,
            date=entity.date,
            main_course=entity.main_course,
            manager=entity.manager,
            created_at=entity.created_at,
        )


class DailyMenuUpdateDTO(BaseModel):
    date: Optional[Date] = None
    main_course: Optional[str] = None

class LeftouversLunchInDTO(BaseModel):
    school: UUID
    leftouvers_kg: int
    amount_students: int
    user: UUID

class LeftouversLunchOutDTO(BaseModel):
    id: UUID
    school: UUID
    leftouvers_kg: int
    amount_students: int
    user: UUID
    created_at: datetime

    @classmethod
    def from_domain(cls, entity):
        return cls(
            id=entity.id,
            school=entity.school.id,
            leftouvers_kg=entity.leftouvers_kg,
            amount_students=entity.amount_students,
            user=entity.user.id,
            created_at=entity.created_at
        )

class LeftouversLunchUpdateDTO(BaseModel):
    leftouvers_kg: Optional[int] = None
    amount_students: Optional[int] = None