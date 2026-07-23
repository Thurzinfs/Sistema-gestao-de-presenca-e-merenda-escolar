from datetime import date as Date, datetime as Datetime
from typing import List
from app.canteen.domain.entities import DailyMenuEntity
from app.canteen.domain.servicies import IPickDatesService, IVerifyLeftouverLunchExistsService
from app.canteen.infrastructure.models import DailyMenu, LeftouversLunch


class PickDatesService(IPickDatesService):
    def pick_dates(
        self, from_date: Date, to_date: Date
    ) -> List[DailyMenuEntity]:
        models = DailyMenu.objects.all()
        dates = [model.date for model in models]
        interval = []
        for date in dates:
            if date >= from_date and date <= to_date:
                interval.append(date)

        models = [DailyMenu.objects.get(date=date) for date in interval]
        return [
            DailyMenuEntity(
                id=model.id,
                school=model.school.id,
                date=model.date,
                main_course=model.main_course,
                manager=model.manager.id,
                created_at=model.created_at,
            )
            for model in models
        ]

class VerifyLeftouverLunchExistsService(IVerifyLeftouverLunchExistsService):
    def verify(self) -> bool:
        today = Datetime.now().date().month
        for model in LeftouversLunch.objects.all():
            date_model = model.created_at.date().month
            if date_model == today:
                return True
        
        return False