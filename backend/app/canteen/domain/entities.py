from datetime import datetime, date as Date
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class DailyMenuEntity:
    id: UUID = field(default_factory=uuid4)
    school: UUID | None = field(default=None)
    date: Date | None = field(default=None)
    main_course: str = field(default='')
    manager: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)

    def change_date(self, date):
        if date:
            self.date = date

    def change_main_course(self, main_course):
        if main_course:
            self.main_course = main_course

@dataclass
class LeftouversLunchEntity:
    id: UUID = field(default_factory=uuid4)
    school: UUID | None = field(default=None)
    leftouvers_kg: int = field(default=0)
    amount_students: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)

    def change_leftouvers_kg(self, leftouvers_kg):
        if leftouvers_kg:
            self.leftouvers_kg = leftouvers_kg

    def change_amount_students(self, amount_students):
        if amount_students:
            self.amount_students = amount_students