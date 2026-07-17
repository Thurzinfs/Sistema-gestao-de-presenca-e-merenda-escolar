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
    date: Date
    main_course: str
    manager: UUID
    created_at: datetime

    @classmethod
    def from_domain(cls, entity):
        return cls(
            id=entity.id,
            date=entity.date,
            main_course=entity.main_course,
            manager=entity.manager,
            created_at=entity.created_at
        )
    
class DailyMenuUpdateDTO(BaseModel):
    date: Optional[UUID] = None
    main_course: Optional[str] = None