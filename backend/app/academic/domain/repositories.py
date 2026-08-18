from abc import abstractmethod, ABC
from typing import List, Optional
from uuid import UUID

from app.academic.domain.entities import ClassroomEntity, StudentsEntity


class IClassroomRepository(ABC):
    @abstractmethod
    def save(self, entity: ClassroomEntity) -> ClassroomEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> ClassroomEntity | None:
        ...

    @abstractmethod
    def find_classroom_by_school(self, school: UUID) -> ClassroomEntity | None:
        ...

    # verification
    @abstractmethod
    def verify_classroom_by_name(self, name: str) -> bool:
        ...

    @abstractmethod
    def list_classroom_active(
        self, active: Optional[bool]
    ) -> List[ClassroomEntity]:
        ...


class IStudentsRepository(ABC):
    @abstractmethod
    def save(self, entity: StudentsEntity) -> StudentsEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> StudentsEntity | None:
        ...

    @abstractmethod
    def find_students_by_classroom(
        self, classroom: UUID
    ) -> StudentsEntity | None:
        ...

    @abstractmethod
    def find_students_by_ra(self, ra: str) -> StudentsEntity | None:
        ...

    # verification
    @abstractmethod
    def verify_students_by_name(self, name: str) -> bool:
        ...

    @abstractmethod
    def verify_students_by_ra(self, ra: str) -> bool:
        ...

    @abstractmethod
    def verify_students_by_qrcode(self, qrcode: str) -> bool:
        ...

    @abstractmethod
    def list_students_active(
        self, active: Optional[bool]
    ) -> List[StudentsEntity]:
        ...

    @abstractmethod
    def list_by_classroom(self, classroom_id: UUID) -> List[StudentsEntity]:
        ...
