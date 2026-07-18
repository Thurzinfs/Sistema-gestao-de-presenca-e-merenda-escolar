from uuid import UUID
from datetime import date as Date
from app.canteen.domain.repositories import IDailyMenuRepository
from app.canteen.domain.entities import DailyMenuEntity
from app.canteen.infrastructure.models import DailyMenu

class DailyMenuRepository(IDailyMenuRepository):
    def save(self, entity: DailyMenuEntity) -> DailyMenuEntity:
        DailyMenu.objects.update_or_create(
            id=entity.id,
            defaults={
                "school_id": entity.school,
                "date": entity.date,
                "main_course": entity.main_course,
                "manager_id": entity.manager,
                "created_at": entity.created_at
            }
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
            created_at=model.created_at
        )