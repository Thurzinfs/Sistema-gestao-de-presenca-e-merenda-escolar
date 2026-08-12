from datetime import datetime

from ninja import Schema

from uuid import UUID

from app.presence.application.dtos import FrequencyInDTO, FrequencyOutDTO, ReadingInDTO, RegisterSnackInDTO, ReadingOutDTO, RegisterSnackOutDTO
from app.presence.domain.role import MomentRole, SnackRole


class ReadingIn(Schema):
    student: UUID
    moment: MomentRole | str

    def to_dto(self):
        return ReadingInDTO(
            student=self.student,
            moment=self.moment
        )
    
class ReadingOut(Schema):
    id: UUID
    student: UUID
    moment: MomentRole | str
    date_time: datetime

    @staticmethod
    def from_domain(model: ReadingOutDTO):
        return ReadingOut(
            id=model.id,
            student=model.student,
            moment=model.moment,
            date_time=model.date_time
        )
    
class FrequencyIn(Schema):
    student: UUID
    date: datetime
    on_time: bool
    reading: UUID

    def to_dto(self) -> FrequencyInDTO:
        return FrequencyInDTO(
            student=self.student,
            date=self.date,
            on_time=self.on_time,
            reading=self.reading
        )

class FrequencyOut(Schema):
    id: UUID
    student: UUID
    date: datetime
    on_time: bool
    reading: UUID 

    @staticmethod
    def from_domain(model: FrequencyOutDTO):
        return FrequencyOut(
            id=model.id,
            student=model.student,
            date=model.date,
            on_time=model.on_time,
            reading=model.reading
        )
    
class FrequencyUpdate(Schema):
    id: UUID | None = None
    student: UUID | None = None
    date: datetime | None = None
    on_time: bool | None = None
    reading: UUID | None = None

class RegisterSnackIn(Schema):
    student: UUID
    date: datetime
    moment: MomentRole | str
    type_snack: SnackRole | str
    reading: UUID

    def to_dto(self):
        return RegisterSnackInDTO(
            student=self.student,
            date=self.date,
            moment=self.moment,
            type_snack=self.type_snack,
            reading=self.reading
        )

class RegisterSnackOut(Schema):
    id: UUID
    student: UUID
    date: datetime
    moment: MomentRole | str
    type_snack: SnackRole | str
    reading: UUID

    @staticmethod
    def from_domain(model: RegisterSnackOutDTO):
        return RegisterSnackOut(
            id=model.id,
            student=model.student,
            date=model.date,
            moment=model.moment,
            type_snack=model.type_snack,
            reading=model.reading
        )
