from typing import Optional
from uuid import UUID
from datetime import datetime, date as Date
from ninja import Schema

from app.canteen.application.dtos import DailyMenuInDTO, DailyMenuUpdateDTO, LeftouversLunchInDTO, LeftouversLunchUpdateDTO


class DailyMenuIn(Schema):
    school: UUID
    date: Date
    main_course: str
    manager: UUID

    def to_dto(self) -> DailyMenuInDTO:
        return DailyMenuInDTO(
            school=self.school,
            date=self.date,
            main_course=self.main_course,
            manager=self.manager,
        )


class DailyMenuOut(Schema):
    id: UUID
    school: UUID
    date: Date
    main_course: str
    manager: UUID
    created_at: datetime

    @staticmethod
    def from_domain(entity):
        return DailyMenuOut(
            id=entity.id,
            school=entity.school,
            date=entity.date,
            main_course=entity.main_course,
            manager=entity.manager,
            created_at=entity.created_at,
        )


class DailyMenuUpdate(Schema):
    date: Optional[Date] = None
    main_course: Optional[str] = None

    def to_dto(self) -> DailyMenuUpdateDTO:
        return DailyMenuUpdateDTO(date=self.date, main_course=self.main_course)

class LeftouversLunchIn(Schema):
    school: UUID
    leftouvers_kg: int
    amount_students: int
    user: UUID

    def to_dto(self) -> LeftouversLunchInDTO:
        return LeftouversLunchInDTO(
            school=self.school,
            leftouvers_kg=self.leftouvers_kg,
            amount_students=self.amount_students,
            user=self.user
        )

class LeftouversLunchOut(Schema):
    id: UUID
    school: UUID
    leftouvers_kg: int
    amount_students: int
    user: UUID
    created_at: datetime

    @staticmethod
    def from_domain(entity):
        return LeftouversLunchOut(
            id=entity.id,
            school=entity.school,
            leftouvers_kg=entity.leftouvers_kg,
            amount_students=entity.amount_students,
            user=entity.user,
            created_at=entity.created_at
        )

class LeftouversLunchUpdate(Schema):
    leftouvers_kg: Optional[int] = None
    amount_students: Optional[int] = None

    def to_dto(self) -> LeftouversLunchUpdateDTO:
        return LeftouversLunchUpdateDTO(
            leftouvers_kg=self.leftouvers_kg,
            amount_students=self.amount_students
        )