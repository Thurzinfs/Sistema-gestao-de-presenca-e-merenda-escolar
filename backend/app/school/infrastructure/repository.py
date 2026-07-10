from typing import List
from uuid import UUID

from app.school.domain.entites import ManagerEntity, SchoolEntity
from app.school.domain.repositories import IManagerRepository, ISchoolRepository
from app.school.infrastructure.models import Manager, School


class DjangoSchoolRepository(ISchoolRepository):
    def save(self, entity: SchoolEntity) -> SchoolEntity:
        School.objects.update_or_create(
            id=id,
            defaults={
                'name': entity.name,
                'time_closing_presence': entity.time_closing_presence,
                'time_send_lunch': entity.time_send_lunch,
                'time_send_snack_afternoon': entity.time_send_snack_afternoon,
                'number_whats': entity.number_whats,
                'created_at': entity.created_at,
                'deleted_at': entity.deleted_at
            }
        )

        return entity
    
    def find_by_id(self, id: UUID) -> SchoolEntity | None:
        try:
            return self._to_model(School.objects.get(id=id))
    
        except School.DoesNotExist:
            return None
        
    def find_by_number_whats(self, number: str) -> SchoolEntity | None:
        try:
            return self._to_model(School.objects.get(number_whats=number))
        
        except School.DoesNotExist:
            return None
        
    def lists_schools_actives(self) -> List[SchoolEntity]:
        try:
            return [
                self._to_model(entity)
                for entity in School.objects.filter(deleted_at__isnull=True).all()
            ]
        
        except School.DoesNotExist:
            return []
        
    def verify_exists_school_by_name(self, name: str) -> bool:
        return Manager.objects.filter(name=name).exists()
    
    def _to_model(self, model: School) -> SchoolEntity:
        return SchoolEntity(
            id=model.id,
            name=model.name,
            time_closing_presence=model.time_closing_presence,
            time_send_lunch=model.time_send_lunch,
            time_send_snack_afternoon=model.time_send_snack_afternoon,
            number_whats=model.number_whats,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )


class DjangoManagerRepository(IManagerRepository):
    def save(self, entity: ManagerEntity) -> ManagerEntity:
        Manager.objects.update_or_create(
            id=id,
            defaults={
                'school_id': entity.school_id,
                'role': entity.role,
                'name': entity.name,
                'email': entity.email,
                'password': entity.password,
                'active': entity.active,
                'created_at': entity.created_at
            }
        )
        
        return entity
    
    def find_by_id(self, id: UUID) -> ManagerEntity | None:
        try:
            return self._to_model(Manager.objects.get(id=id))

        except Manager.DoesNotExist:
            return None
        
    def find_by_email(self, email: str) -> ManagerEntity | None:
        try:
            return self._to_model(Manager.objects.get(email=email))

        except Manager.DoesNotExist:
            return None
    
    def lists_managers_by_actives(self) -> List[ManagerEntity]:
        try:
            return [
                self._to_model(entity)
                for entity in Manager.objects.filter(active=True).all()
            ]
        
        except Manager.DoesNotExist:
            return []
        
    def lists_managers_role_by_role(self, role: str) -> List[ManagerEntity]:
        try:
            return [
                self._to_model(entity)
                for entity in Manager.objects.filter(role=role)
            ]
        
        except Manager.DoesNotExist:
            return []

    def _to_model(self, model: Manager) -> ManagerEntity:
        return ManagerEntity(
            id=model.id,
            school_id=model.school_id,
            role=model.role,
            email=model.email,
            password=model.password,
            active=model.active,
            created_at=model.created_at
        )
    