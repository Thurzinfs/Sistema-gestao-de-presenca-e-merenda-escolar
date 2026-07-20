from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID
from app.canteen.domain.entities import DailyMenuEntity


class IDailyMenuRepository(ABC):
    @abstractmethod
    def save(self, daily_menu: DailyMenuEntity) -> DailyMenuEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> DailyMenuEntity | None:
        ...

    @abstractmethod
    def find_by_date(self, date: date) -> DailyMenuEntity | None:
        ...

    @abstractmethod
    def verify_exists(self, id: UUID) -> bool:
        ...

    @abstractmethod
    def verify_by_date(self, date: date) -> bool:
        ...
