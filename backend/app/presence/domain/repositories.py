from abc import ABC,abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID

from django.contrib.gis.measure import A

from app.presence.domain.entities import FrequencyEntity, ReadingEntity, RegisterSnackEntity
from app.presence.domain.role import MomentRole, SnackRole

class IReadingRepository(ABC):
    @abstractmethod
    def save(self, entity: ReadingEntity) -> ReadingEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> ReadingEntity | None:
        ...

    @abstractmethod
    def very_exists(self, id: UUID) -> bool:
        ...

    @abstractmethod
    def list_readings_all(self) -> List[ReadingEntity]:
        ...

    @abstractmethod
    def very_exists_by_student_id(self, student_id: UUID) -> bool:
        ...

class IFrequencyRepository(ABC):
    @abstractmethod
    def save(self, entity: FrequencyEntity) -> FrequencyEntity:
        ...

    @abstractmethod
    def list_frequency_all(self) -> List[FrequencyEntity]:
        ...

    @abstractmethod
    def very_exists_frequency_by_id(self, frequency_id: UUID) -> bool:
        ...

    @abstractmethod
    def _to_model(self, model: FrequencyEntity) -> FrequencyEntity:
        ...

class IRegisterSnackRepository(ABC):
    @abstractmethod
    def save(self, entity: RegisterSnackEntity) -> RegisterSnackEntity:
        ...


    @abstractmethod
    def very_exist_register_snack_by_student_id(self, student_id: UUID) -> bool:
        ...

    @abstractmethod
    def list_register_snack_all(self) -> List[RegisterSnackEntity]:
        ...

    @abstractmethod
    def list_register_snack_by_date(self, date: datetime) -> List[RegisterSnackEntity]:
        ...

    @abstractmethod
    def list_register_snack_by_moment(self, moment: MomentRole) -> List[RegisterSnackEntity]:
        ...

    @abstractmethod
    def list_register_snack_by_type_snack(self, type_snack: SnackRole) -> List[RegisterSnackEntity]:
        ...

    @abstractmethod
    def _to_model(self, model: RegisterSnackEntity) -> RegisterSnackEntity:
        ...
