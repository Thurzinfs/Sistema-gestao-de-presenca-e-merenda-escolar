
from pydantic import BaseModel
from uuid import UUID
from datetime import date as Date, datetime
from app.presence.domain.role import MomentRole, SnackRole

class ReadingInDTO(BaseModel):
    student: UUID
    moment: MomentRole | str

class ReadingOutDTO(BaseModel):
    id: UUID
    student: UUID
    moment: MomentRole | str
    date_time: datetime

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            student=model.student,
            moment=model.moment,
            date_time=model.date_time
        )

class FrequencyInDTO(BaseModel):
    student: UUID
    date: Date
    on_time: bool
    reading: UUID

class FrequencyOutDTO(BaseModel):
    id: UUID
    student: UUID
    date: Date
    on_time: bool
    reading: UUID

    @classmethod
    def from_domain(cls, entity):
        return cls(
            id=entity.id,
            student=entity.student,
            date=entity.date,
            on_time=entity.on_time,
            reading=entity.reading
        )

class RegisterSnackInDTO(BaseModel):
    student: UUID
    date: Date
    moment: MomentRole | str
    type_snack: SnackRole | str
    reading: UUID

class RegisterSnackOutDTO(BaseModel):
    id: UUID
    student: UUID
    date: Date
    moment: MomentRole | str
    type_snack: SnackRole | str
    reading: UUID

    @classmethod
    def from_domain(cls, entity):
        return cls(
            id=entity.id,
            student=entity.student,
            date=entity.date,
            moment=entity.moment,
            type_snack=entity.type_snack,
            reading=entity.reading
        )