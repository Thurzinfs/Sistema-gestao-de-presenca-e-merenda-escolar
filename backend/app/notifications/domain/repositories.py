from abc import ABC, abstractmethod
from datetime import date
from typing import List
from uuid import UUID

from app.notifications.domain.entities import WahaMessageEntity


class IWhatsAppMessageRepository(ABC):
    @abstractmethod
    def save(self, entity: WahaMessageEntity) -> WahaMessageEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> WahaMessageEntity | None:
        ...

    @abstractmethod
    def find_by_school_and_moment(self, school: UUID, moment: str) -> List[WahaMessageEntity]:
        ...

    @abstractmethod
    def exists_for_today(self, school: UUID, moment: str, date: date) -> bool:
        ...
