from typing import Optional, List
from uuid import UUID

from app.academic.domain.repositories import (
    IClassroomRepository,
    IStudentsRepository,
)
from app.school.domain.exceptions import SchoolNotFoundException
from app.school.domain.repositories import ISchoolRepository
from app.academic.domain.entities import ClassroomEntity, StudentsEntity

from app.academic.application.dtos import (
    ClassroomInDTO,
    ClassroomOutDTO,
    ClassroomUpdateDTO,
    StudentsInDTO,
    StudentsOutDTO,
    StudentsUpdateDTO,
)
from app.academic.domain.exceptions import (
    ClassroomAlreadyExistsException,
    ClassroomNotActiveException,
    ClassroomNotFoundException,
    StudentAlreadyExistsException,
    StudentsNotFoundException,
)


class RegisterClassroomUsercase:
    def __init__(
        self,
        classroom_repo: IClassroomRepository,
        school_repo: ISchoolRepository,
    ) -> None:
        self.classroom_repo = classroom_repo
        self.school_repo = school_repo

    def execute(self, dto: ClassroomInDTO) -> ClassroomOutDTO:
        if self.school_repo.find_by_id(id=dto.school) is None:
            raise SchoolNotFoundException('School not found')

        if self.classroom_repo.verify_classroom_by_name(dto.name):
            raise ClassroomAlreadyExistsException('This School already exists')

        classroom = ClassroomEntity(school=dto.school, name=dto.name)
        self.classroom_repo.save(classroom)
        return ClassroomOutDTO.from_domain(classroom)


class ResponseClassroomUseCase:
    def __init__(self, classroom_repo: IClassroomRepository) -> None:
        self.classroom_repo = classroom_repo

    def execute(self, id: UUID) -> ClassroomOutDTO:
        classroom = self.classroom_repo.find_by_id(id)
        if classroom is None:
            raise ClassroomNotFoundException('Classroom not found')

        if not classroom.active:
            raise ClassroomNotActiveException('Classroom not active')

        return ClassroomOutDTO.from_domain(classroom)


class ClassroomUpdateUseCase:
    def __init__(
        self,
        classroom_repo: IClassroomRepository,
        school_repo: ISchoolRepository,
    ) -> None:
        self.classroom_repo = classroom_repo
        self.school_repo = school_repo

    def execute(self, id: UUID, dto: ClassroomUpdateDTO) -> ClassroomOutDTO:
        classroom = self.classroom_repo.find_by_id(id)
        if not classroom:
            raise ClassroomNotFoundException('Classroom not found')

        if dto.name:
            if self.classroom_repo.verify_classroom_by_name(dto.name):
                raise ClassroomAlreadyExistsException(
                    'This classroom name exists'
                )
            classroom.name = dto.name

        self.classroom_repo.save(classroom)
        return ClassroomOutDTO.from_domain(classroom)


class ListClassroomUseCase:
    def __init__(self, classroom_repo: IClassroomRepository) -> None:
        self.classroom_repo = classroom_repo

    def execute(self, active: Optional[bool]) -> List[ClassroomOutDTO]:
        classrooms = self.classroom_repo.list_classroom_active(active=active)
        return [
            ClassroomOutDTO.from_domain(classroom) for classroom in classrooms
        ]


class DeactiveClassroomUseCase:
    def __init__(self, classroom_repo: IClassroomRepository) -> None:
        self.classroom_repo = classroom_repo

    def execute(self, id: UUID) -> ClassroomOutDTO:
        classroom = self.classroom_repo.find_by_id(id)
        if not classroom:
            raise ClassroomNotFoundException('Classroom not found')

        classroom.deactivate()
        self.classroom_repo.save(classroom)
        return ClassroomOutDTO.from_domain(classroom)


class RegisterStudentsUseCase:
    def __init__(
        self,
        students_repo: IStudentsRepository,
        classroom_repo: IClassroomRepository,
    ) -> None:
        self.students_repo = students_repo
        self.classroom_repo = classroom_repo

    def execute(self, dto: StudentsInDTO) -> StudentsOutDTO:
        classroom = self.classroom_repo.find_by_id(id=dto.classroom)
        if classroom is None:
            raise ClassroomNotFoundException('Classroom not found')

        if not classroom.active:
            raise ClassroomNotActiveException('Classroom not active')

        if self.students_repo.verify_students_by_ra(ra=dto.ra):
            raise StudentAlreadyExistsException('This RA already exists')

        student = StudentsEntity(
            classroom=dto.classroom,
            name=dto.name,
            ra=dto.ra,
            qr_code=dto.qr_code,
        )
        salved = self.students_repo.save(student)
        return StudentsOutDTO.from_domain(salved)


class ResponseStudentsUseCase:
    def __init__(self, students_repo: IStudentsRepository) -> None:
        self.students_repo = students_repo

    def execute(self, id: UUID) -> StudentsOutDTO:
        students = self.students_repo.find_by_id(id)
        if students is None:
            raise StudentsNotFoundException('Student not found')

        if students.active is False:
            raise StudentsNotFoundException('Student not active')

        return StudentsOutDTO.from_domain(students)


class StudentsUpdateUseCase:
    def __init__(self, students_repo: IStudentsRepository) -> None:
        self.students_repo = students_repo

    def execute(self, id: UUID, dto: StudentsUpdateDTO) -> StudentsOutDTO:
        student = self.students_repo.find_by_id(id)
        if student is None:
            raise StudentsNotFoundException('Student not found')

        if dto.name:
            student.change_name(dto.name)

        if dto.ra:
            if self.students_repo.verify_students_by_ra(ra=dto.ra):
                raise StudentAlreadyExistsException('This RA already exists')

            student.change_ra(dto.ra)

        if dto.qr_code:
            student.change_qr_code(dto.qr_code)

        saved = self.students_repo.save(student)
        return StudentsOutDTO.from_domain(saved)


class ListStudentsUseCase:
    def __init__(self, students_repo: IStudentsRepository) -> None:
        self.students_repo = students_repo

    def execute(self, active: Optional[bool]) -> List[StudentsOutDTO]:
        students = self.students_repo.list_students_active(active=active)
        return [StudentsOutDTO.from_domain(student) for student in students]

class ListStudentsByClassroom:
    def __init__(self, students_repo: IStudentsRepository) -> None:
        self.students_repo = students_repo

    def execute(self, classroom_id: UUID) -> List[StudentsOutDTO]:
        entities = self.students_repo.list_by_classroom(classroom_id)
        return [StudentsOutDTO.from_domain(entity) for entity in entities]

class DeactiveStudentsUseCase:
    def __init__(self, students_repo: IStudentsRepository) -> None:
        self.students_repo = students_repo

    def execute(self, id: UUID) -> StudentsOutDTO:
        students = self.students_repo.find_by_id(id)
        if not students:
            raise StudentsNotFoundException('Students not found')

        students.deactive()
        self.students_repo.save(students)
        return StudentsOutDTO.from_domain(students)
