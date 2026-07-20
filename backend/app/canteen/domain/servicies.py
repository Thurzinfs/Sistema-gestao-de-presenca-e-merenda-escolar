from abc import ABC, abstractmethod
from datetime import date
from typing import List
from app.canteen.domain.entities import DailyMenuEntity

class IPickDatesService(ABC):
    @abstractmethod
    def pick_dates(self, from_date: date, to_date: date) -> List[DailyMenuEntity]:
        ...