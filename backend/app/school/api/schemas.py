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
