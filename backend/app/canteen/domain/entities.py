from datetime import datetime, date
from dataclasses import dataclass
from uuid import UUID

@dataclass
class DailyMenuEntity:
    id: UUID
    school: UUID
    date: date
    main_course: str
    manager: UUID
    created_at: datetime