from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.school.domain.entites import ManagerEntity, SchoolEntity


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
    def verify_exists_school_by_name(self, name: str) -> bool:
        ...
    
    @abstractmethod
    def lists_schools_actives(self) -> List[SchoolEntity]:
        ...


class IManagerRepository(ABC):
    @abstractmethod
    def save(self, entity: ManagerEntity) -> ManagerEntity:
        ...
    
    @abstractmethod
    def find_by_id(self, id: UUID) -> ManagerEntity | None:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> ManagerEntity | None:
        ...
    
    @abstractmethod
    def lists_managers_role_by_role(self, role: str) -> List[ManagerEntity]:
        ...

    @abstractmethod
    def lists_managers_by_actives(self) -> List[ManagerEntity]:
        ...
    