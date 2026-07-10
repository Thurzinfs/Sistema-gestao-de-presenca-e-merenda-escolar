from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.school.domain.entites import SchoolEntity


class ISchoolRepository(ABC):
    @abstractmethod
    def save(self, entity: SchoolEntity) -> SchoolEntity:
        ...
    
    @abstractmethod
    def find_by_id(self, id: UUID) -> SchoolEntity | None:
        ...

    @abstractmethod
    def find_by_number_whats(self, number: str) -> SchoolEntity | None:
        ...
    
    @abstractmethod
    def lists_schools_actives(self) -> List[SchoolEntity]:
        ...
