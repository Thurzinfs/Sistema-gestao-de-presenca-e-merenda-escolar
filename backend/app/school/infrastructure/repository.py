from typing import List
from uuid import UUID

from app.school.domain.entites import ManagerEntity, RefreshTokenEntity, SchoolEntity
from app.school.domain.repositories import IManagerRepository, IRefreshTokenRepository, ISchoolRepository
from app.school.domain.value_objects import SchoolTimeVO
from app.school.infrastructure.models import Manager, RefreshToken, School


class DjangoSchoolRepository(ISchoolRepository):
    def save(self, entity: SchoolEntity) -> SchoolEntity:
        School.objects.update_or_create(
            id=entity.id,
            defaults={
                'name': entity.name,
                'time_closing_presence': entity.time_closing_presence.value
                if entity.time_closing_presence
                else None,
                'time_send_lunch': entity.time_send_lunch.value
                if entity.time_send_lunch
                else None,
                'time_send_snack_afternoon': entity.time_send_snack_afternoon.value
                if entity.time_send_snack_afternoon
                else None,
                'number_whats': entity.number_whats,
                'created_at': entity.created_at,
                'deleted_at': entity.deleted_at,
            },
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
                for entity in School.objects.filter(
                    deleted_at__isnull=True
                ).all()
            ]

        except School.DoesNotExist:
            return []

    def verify_exists_school_by_name(self, name: str) -> bool:
        return School.objects.filter(name=name).exists()

    def _to_model(self, model: School) -> SchoolEntity:
        return SchoolEntity(
            id=model.id,
            name=model.name,
            time_closing_presence=SchoolTimeVO(model.time_closing_presence),
            time_send_lunch=SchoolTimeVO(model.time_send_lunch),
            time_send_snack_afternoon=SchoolTimeVO(
                model.time_send_snack_afternoon
            ),
            number_whats=model.number_whats,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
        )


class DjangoManagerRepository(IManagerRepository):
    def save(self, entity: ManagerEntity) -> ManagerEntity:
        Manager.objects.update_or_create(
            id=entity.id,
            defaults={
                'school_id': entity.school,
                'role': entity.role,
                'name': entity.name,
                'email': entity.email,
                'password': entity.password,
                'active': entity.active,
                'created_at': entity.created_at,
            },
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
            school=model.school.id,
            name=model.name,
            role=model.role,
            email=model.email,
            password=model.password,
            active=model.active,
            created_at=model.created_at,
        )
    

class DjangoRefreshTokenRepository(IRefreshTokenRepository):
    def save(self, entity: RefreshTokenEntity) -> RefreshTokenEntity:
        RefreshToken.objects.update_or_create(
            id=entity.id,
            defaults={
                'token': entity.token,
                'revoked': entity.revoked,
                'user_id': entity.user,
                'created_at': entity.created_at,
                'expire_at': entity.expire_at
            }
        )

        return entity
    
    def find_by_hash(self, hash: str) -> RefreshTokenEntity | None:
        try:
            return self._to_model(RefreshToken.objects.get(token=hash))

        except RefreshToken.DoesNotExist:
            return None
        
    def revoke_all_by_user(self, user_id: UUID) -> None:
        RefreshToken.objects.filter(user=user_id).update(revoked=True)
    
    def _to_model(self, model: RefreshToken) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            id=model.id,
            token=model.token,
            revoked=model.revoked,
            user=model.user.id,
            created_at=model.created_at,
            expire_at=model.expire_at
        )
