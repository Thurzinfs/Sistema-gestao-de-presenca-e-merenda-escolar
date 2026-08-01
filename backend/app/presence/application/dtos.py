
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from app.presence.domain.role import MomentRole, SnackRole

class ReadingInDTO(BaseModel):
    student_id: UUID
    moment: MomentRole | str

class ReadingOutDTO:
    id: UUID
    student_id: UUID
    moment: MomentRole | str
    date_time: datetime

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            student_id=model.student_id,
            moment=model.moment,
            date_time=model.date_time
        )

class FrequencyInDTO(BaseModel):
    student_id: UUID
    date: datetime
    on_time: bool
    reading_id: UUID

class FrequencyOutDTO(BaseModel):
    id: UUID
    student_id: UUID
    date: datetime
    on_time: bool
    reading_id: UUID

    @classmethod
    def from_domain(cls, entity):
        return cls(
            id=entity.id,
            student_id=entity.student_id,
            date=entity.date,
            on_time=entity.on_time,
            reading_id=entity.reading_id
        )

class RegisterSnackInDTO(BaseModel):
    student_id: UUID
    date: datetime
    moment: MomentRole | str
    type_snack: SnackRole
    reading_id: UUID

class RegisterSnackOutDTO(BaseModel):
    id: UUID
    student_id: UUID
    date: datetime
    moment: MomentRole | str
    type_snack: SnackRole
    reading_id: UUID

    @classmethod
    def from_domain(cls, entity):
        return cls(
            id=entity.id,
            student_id=entity.id,
            date=entity.data,
            moment=entity.moment,
            type_snack=entity.type_snack
        )