from typing import Optional
from uuid import UUID
from datetime import datetime, date as Date
from ninja import Schema

from app.canteen.application.dtos import DailyMenuInDTO, DailyMenuUpdateDTO

class DailyMenuIn(Schema):
    school: UUID
    date: Date
    main_course: str
    manager: UUID

    def to_dto(self) -> DailyMenuInDTO:
        return DailyMenuInDTO(
            school = self.school,
            date = self.date,
            main_course = self.main_course,
            manager = self.manager
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
            created_at=entity.created_at
        )

class DailyMenuUpdate(Schema):
    date: Optional[Date] = None
    main_course: Optional[str] = None

    def to_dto(self) -> DailyMenuUpdateDTO:
        return DailyMenuUpdateDTO(
            date=self.date,
            main_course=self.main_course
        )
