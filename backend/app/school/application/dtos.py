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
