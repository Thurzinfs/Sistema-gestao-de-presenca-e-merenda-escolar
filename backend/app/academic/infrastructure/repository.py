from typing import List
from uuid import UUID

from app.academic.domain.entities import ClassroomEntity, StudentsEntity
from app.academic.infrastructure.models import Classroom, Student
from app.academic.domain.repositories import (
    IClassroomRepository,
    IStudentsRepository,
)


class ClassroomRepository(IClassroomRepository):
    def save(self, entity: ClassroomEntity) -> ClassroomEntity:
        Classroom.objects.update_or_create(
            id=entity.id,
            defaults={
                'school_id': entity.school,
                'name': entity.name,
                'active': entity.active,
                'created_at': entity.created_at,
            },
        )
        return entity

    def find_by_id(self, id: UUID) -> ClassroomEntity | None:
        try:
            return self._to_entity(Classroom.objects.get(id=id))
        except Classroom.DoesNotExist:
            return None

    def find_classroom_by_school(self, school: UUID) -> ClassroomEntity | None:
        try:
            return self._to_entity(Classroom.objects.get(school=school))
        except Classroom.DoesNotExist:
            return None

    def verify_classroom_by_name(self, name: str) -> bool:
        return Classroom.objects.filter(name=name).exists()

    def list_classroom_active(
        self, active: bool | None
    ) -> List[ClassroomEntity]:
        qs = Classroom.objects.all()
        if active is not None:
            qs = qs.filter(active=active)
        return [self._to_entity(classroom) for classroom in qs]

    def _to_entity(self, model: Classroom) -> ClassroomEntity:
        return ClassroomEntity(
            id=model.id,
            school=model.school.id,
            name=model.name,
            active=model.active,
            created_at=model.created_at,
        )


class StudentsRepository(IStudentsRepository):
    def save(self, entity: StudentsEntity) -> StudentsEntity:
        Student.objects.update_or_create(
            id=entity.id,
            defaults={
                'classroom_id': entity.classroom,
                'name': entity.name,
                'ra': entity.ra,
                'active': entity.active,
                'qr_code': entity.qr_code,
                'created_at': entity.created_at,
                'active': entity.active,
            },
        )
        return entity

    def find_by_id(self, id: UUID) -> StudentsEntity | None:
        try:
            return self._to_entity(Student.objects.get(id=id))
        except Student.DoesNotExist:
            return None

    def find_students_by_classroom(
        self, classroom: UUID
    ) -> StudentsEntity | None:
        try:
            return self._to_entity(Student.objects.get(classroom=classroom))
        except Student.DoesNotExist:
            return None

    def find_students_by_ra(self, ra: str) -> StudentsEntity | None:
        try:
            return self._to_entity(Student.objects.get(ra=ra))
        except Student.DoesNotExist:
            return None

    def list_students_active(self, active: bool) -> List[StudentsEntity]:
        qs = Student.objects.all()
        if active is not None:
            qs = qs.filter(active=active)
        return [self._to_entity(students) for students in qs]

    def verify_students_by_name(self, name: str) -> bool:
        return Student.objects.filter(name=name).exists()

    def verify_students_by_ra(self, ra: str) -> bool:
        return Student.objects.filter(ra=ra).exists()

    def verify_students_by_qrcode(self, qrcode: str) -> bool:
        return Student.objects.filter(qrcode=qrcode).exists()

    def _to_entity(self, model: Student) -> StudentsEntity:
        return StudentsEntity(
            id=model.id,
            classroom=model.classroom.id,
            name=model.name,
            ra=model.ra,
            qr_code=model.qr_code,
            created_at=model.created_at,
            active=model.active
        )
