from datetime import date
from typing import List
from uuid import UUID

from app.notifications.domain.entities import WahaMessageEntity
from app.notifications.domain.repositories import IWhatsAppMessageRepository
from app.notifications.infrastructure.models import WhatsAppMessage


class DjangoWhatsAppMessageRepository(IWhatsAppMessageRepository):
    def save(self, entity: WahaMessageEntity) -> WahaMessageEntity:
        WhatsAppMessage.objects.update_or_create(
            id=entity.id,
            defaults={
                'school_id': entity.school,
                'moment': entity.moment,
                'date': entity.date,
                'number': entity.number,
                'status': entity.status,
                'message': entity.message,
                'created_at': entity.created_at,
            }
        )
        return entity

    def find_by_id(self, id: str) -> WahaMessageEntity | None:
        try:
            return self._to_entity(WhatsAppMessage.objects.get(id=id))
        
        except WhatsAppMessage.DoesNotExist:
            return None

    def find_by_school_and_moment(self, school: UUID, moment: str) -> List[WahaMessageEntity]:
        return [self._to_entity(model) for model in WhatsAppMessage.objects.filter(school=school, moment=moment)]  

    def exists_for_today(self, school: UUID, moment: str, date: date) -> bool:
        return WhatsAppMessage.objects.filter(school=school, moment=moment, date=date).exists()      

    def _to_entity(self, model: WhatsAppMessage) -> WahaMessageEntity:
        return WahaMessageEntity(
            id=model.id,
            school=model.school,
            moment=model.moment,
            date=model.date,
            number=model.number,
            status=model.status,
            message=model.message,
            created_at=model.created_at
        )
