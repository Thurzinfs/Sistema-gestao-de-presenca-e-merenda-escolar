from abc import ABC, abstractmethod
from datetime import date, datetime as Datetime
from uuid import UUID
from app.canteen.domain.entities import DailyMenuEntity, LeftouversLunchEntity


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

class ILeftouversLunchRepository(ABC):
    @abstractmethod
    def save(self, leftouvers_lunch: LeftouversLunchEntity) -> LeftouversLunchEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> LeftouversLunchEntity | None:
        ...

    @abstractmethod
    def find_by_month(self, month: int) -> LeftouversLunchEntity | None:
        ...
