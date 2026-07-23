from uuid import UUID
from datetime import date as Date
from app.canteen.domain.repositories import IDailyMenuRepository, ILeftouversLunchRepository
from app.canteen.domain.entities import DailyMenuEntity, LeftouversLunchEntity
from app.canteen.infrastructure.models import DailyMenu, LeftouversLunch


class DailyMenuRepository(IDailyMenuRepository):
    def save(self, entity: DailyMenuEntity) -> DailyMenuEntity:
        DailyMenu.objects.update_or_create(
            id=entity.id,
            defaults={
                'school_id': entity.school,
                'date': entity.date,
                'main_course': entity.main_course,
                'manager_id': entity.manager,
                'created_at': entity.created_at,
            },
        )
        return entity

    def find_by_id(self, id: UUID) -> DailyMenuEntity | None:
        try:
            return self.to_model(DailyMenu.objects.get(id=id))
        except DailyMenu.DoesNotExist:
            return None

    def find_by_date(self, date: Date) -> DailyMenuEntity | None:
        try:
            return self.to_model(DailyMenu.objects.get(date=date))
        except DailyMenu.DoesNotExist:
            return None

    def verify_exists(self, id: UUID) -> bool:
        return DailyMenu.objects.filter(id=id).exists()

    def verify_by_date(self, date: Date) -> bool:
        return DailyMenu.objects.filter(date=date).exists()

    def to_model(self, model: DailyMenu) -> DailyMenuEntity:
        return DailyMenuEntity(
            id=model.id,
            school=model.school.id,
            date=model.date,
            main_course=model.main_course,
            manager=model.manager.id,
            created_at=model.created_at,
        )

class LeftouversLunchRepository(ILeftouversLunchRepository):
    def save(self, entity: LeftouversLunchEntity) -> LeftouversLunchEntity:
        LeftouversLunch.objects.update_or_create(
            id=entity.id,
            defaults={
                'school_id': entity.school,
                'leftouvers_kg': entity.leftouvers_kg,
                'amount_students': entity.amount_students,
                'user_id': entity.user,
                'created_at': entity.created_at
            }
        )
        return entity

    def find_by_id(self, id: UUID) -> LeftouversLunchEntity:
        try:
            return self.to_model(LeftouversLunch.objects.get(id=id))
        except LeftouversLunch.DoesNotExist:
            return None

    def find_by_month(self, month: int) -> LeftouversLunchEntity | None:
        for model in LeftouversLunch.objects.all():
            if model.created_at.date().month == month:
                return self.to_model(model)
        return None

    def to_model(self, model: LeftouversLunch) -> LeftouversLunchEntity:
        return LeftouversLunchEntity(
            id=model.id,
            school=model.school.id,
            leftouvers_kg=model.leftouvers_kg,
            amount_students=model.amount_students,
            user=model.user.id,
            created_at=model.created_at
        )