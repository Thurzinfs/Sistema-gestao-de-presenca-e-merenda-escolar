from datetime import date, datetime

from typing import List
from uuid import UUID

from app.presence.domain.entities import FrequencyEntity, ReadingEntity, RegisterSnackEntity
from app.presence.domain.repositories import IFrequencyRepository, IReadingRepository, IRegisterSnackRepository
from app.presence.infrastructure.models import Frequency, Readings, RegisterSnack
from app.presence.domain.role import MomentRole, SnackRole
from backend.app.presence.api.schema import RegisterSnackOut

class ReadingRepository(IReadingRepository):
    def save(self, entity: ReadingEntity) -> ReadingEntity:
        Readings.objects.update_or_create(
            id=entity.id,
            defaults={
                'student_id': entity.student_id,
                'moment': entity.moment,
                'date_time': entity.date_time
            }

        )

        return entity
    
    def find_by_id(self, id: UUID) -> ReadingEntity:
        return self._to_model(Readings.objects.get(id=id))
    
    def very_exists(self, id: UUID) -> bool:
        return Readings.objects.filter(id=id).exists()
    
    def list_readings_all(self) -> List[ReadingEntity]:
        return [self._to_model(reading) for reading in Readings.objects.all()]

    def _to_model(self, model) -> ReadingEntity:
        return ReadingEntity(
            id=model.id,
            student_id=model.student_id.id,
            moment=model.moment,
            date_time=model.date_time
        )
    
    def very_exists_by_student_id(self, student_id) -> bool:
        return Readings.objects.filter(student_id=student_id).exists()

class FrequencyRepository(IFrequencyRepository):
    def save(self, entity) -> FrequencyEntity:
        Frequency.objects.update_or_create(
            id=entity.id,
            defaults={
                'student_id': entity.student_id,
                'date': entity.date,
                'on_time': entity.on_time,
                'reading_id': entity.reading_id
            }
        )

        return entity

    def list_frequency_all(self) -> List[FrequencyEntity]:
        try:
            return [self._to_model(frequency) for frequency in Frequency.objects.all()]
        except Frequency.DoesNotExist:
            raise Exception('No Frequency found')

    def very_exists_frequency_by_id(self, frequency_id: UUID) -> bool:
        return Frequency.objects.filter(id=frequency_id).exists()

    def _to_model(self, model) -> FrequencyEntity:
        return FrequencyEntity(
            id=model.id,
            student_id=model.student_id.id,
            date=model.date,
            on_time=model.on_time,
            reading_id=model.reading_id.id
        )

class RegisterSnackRepository(IRegisterSnackRepository):
    def save(self, entity: RegisterSnackEntity) -> RegisterSnackEntity:
        RegisterSnack.objects.update_or_create(
            id=entity.id,
            defaults={
                'student_id':entity.student_id,
                'date': entity.date,
                'type_snack': entity.type_snack,
                'reading_id': entity.reading_id
            }
        )

        return entity

    def very_exist_register_snack_by_student_id(self, student_id: UUID) -> bool:
        return RegisterSnack.objects.filter(student_id=student_id).exists()

    def list_register_snack_by_date(self, date: datetime) -> List[RegisterSnackOut]:
        try:
            return [self._to_model(register_snack) for register_snack in RegisterSnack.objects.filter(date=datetime).get().all()]
        except RegisterSnack.DoesNotExist:
            return []

    def list_register_snack_by_moment(self, moment: MomentRole) -> List[RegisterSnackOut]:
        try:
            return [self._to_model(register_snack) for register_snack in RegisterSnack.objects.filter(moment=moment).get().all()]
        except RegisterSnack.DoesNotExist:
            return []


    def list_register_snack_by_type_snack(self, type_snack: SnackRole) -> List[RegisterSnackOut]:
        try:
            return [self._to_model(register_snack) for register_snack in RegisterSnack.objects.filter(type_snack=type_snack).get().all()]
        except RegisterSnack.DoesNotExist:
            return []

    def _to_model(self, model):
        return RegisterSnackEntity(
            id=model.id,
            student_id=model.id,
            date=model.date,
            moment=model.moment,
            type_snack=model.type_snack,
            reading_id=model.reading_id.id
        )