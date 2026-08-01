from datetime import datetime

from ninja import Schema

from uuid import UUID

from app.academic.models import Student
from app.presence.application.dtos import FrequencyInDTO, ReadingInDTO, RegisterSnackInDTO, ReadingOutDTO
from app.presence.domain.role import MomentRole, SnackRole


class ReadingIn(Schema):
    student_id: UUID
    moment: MomentRole | str

    def to_dto(self):
        return ReadingInDTO(
            student_id=self.student_id,
            moment=self.moment
        )
    
class ReadingOut(Schema):
    id: UUID
    student_id: UUID
    moment: MomentRole | str
    date_time: datetime

    @staticmethod
    def from_domain(model):
        return ReadingOut(
            id=model.id,
            student_id=model.student_id,
            moment=model.moment,
            date_time=model.date_time
        )
    
class FrequencyIn(Schema):
    student_id: UUID
    date: datetime
    on_time: bool
    reading_id: UUID

    def to_dto(self) -> FrequencyInDTO:
        return FrequencyInDTO(
            student_id=self.student_id,
            date=self.date,
            on_time=self.on_time,
            reading_id=self.reading_id
        )

class FrequencyOut(Schema):
    id: UUID
    student_id: UUID
    date: datetime
    on_time: bool
    reading_id: UUID 

    def from_domain(model):
        return FrequencyOut(
            id=model.id,
            student_id=model.student_id,
            date=model.date,
            on_time=model.on_time,
            reading_id=model.reading_id
        )
    
class FrequencyUpdate(Schema):
    id: UUID | None = None
    student_id: UUID | None = None
    date: datetime | None = None
    on_time: bool | None = None
    reading_id: UUID | None = None

class RegisterSnackIn(Schema):
    student_id: UUID
    date: datetime
    moment: MomentRole | str
    type_snack: SnackRole
    reading_id: UUID

    def to_dto(self):
        return RegisterSnackInDTO(
            student_id=self.student_id,
            date=self.date,
            moment=self.moment,
            type_snack=self.type_snack,
            reading_id=self.reading_id
        )

class RegisterSnackOut(Schema):
    id: UUID
    student_id: UUID
    date: datetime
    moment: MomentRole | str
    type_snack: SnackRole
    reading_id: UUID

    def from_domain(self, model):
        return FrequencyOut(
            id=model.id,
            student_id=model.student_id,
            date=model.datetime,
            moment=model.moment,
            type_snack=model.type_snack
        )