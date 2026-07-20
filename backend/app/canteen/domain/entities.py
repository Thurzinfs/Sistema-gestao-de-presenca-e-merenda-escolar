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
