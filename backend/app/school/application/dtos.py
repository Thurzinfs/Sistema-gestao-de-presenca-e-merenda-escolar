from datetime import datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.school.domain.role import ManagerRole


class SchoolInDTO(BaseModel):
    name: str
    time_closing_presence: time
    time_send_lunch: time
    time_send_snack_afternoon: time
    number_whats: str


class SchoolOutDTO(BaseModel):
    id: UUID 
    name: str 
    time_closing_presence: time 
    time_send_lunch: time 
    time_send_snack_afternoon: time 
    number_whats: str 
    created_at: datetime 
    deleted_at: datetime 

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            time_closing_presence=model.time_closing_presence,
            time_send_lunch=model.time_send_lunch,
            time_send_snack_afternoon=model.time_send_snack_afternoon,
            number_whats=model.number_whats,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )


class SchoolInUpdateDTO(BaseModel):
    name: Optional[str] = None
    time_closing_presence: Optional[time] = None
    time_send_lunch: Optional[time] = None
    time_send_snack_afternoon: Optional[time] = None
    number_whats: Optional[str] = None


class ManagerInDTO(BaseModel):
    school_id: UUID
    role: ManagerRole | str
    name: str
    email: EmailStr | str
    password: str

