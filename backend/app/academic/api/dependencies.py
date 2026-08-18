from dependency_injector import containers, providers

from app.academic.application.use_case import (
    ClassroomUpdateUseCase,
    DeactiveClassroomUseCase,
    DeactiveStudentsUseCase,
    ListStudentsUseCase,
    RegisterClassroomUsercase,
    RegisterStudentsUseCase,
    ResponseClassroomUseCase,
    ListClassroomUseCase,
    ResponseStudentsUseCase,
    StudentsUpdateUseCase,
)
from app.academic.infrastructure.repository import (
    ClassroomRepository,
    StudentsRepository,
)
from app.school.infrastructure.repository import DjangoSchoolRepository


class AcademicContainer(containers.DeclarativeContainer):
    classroom_repo = providers.Factory(ClassroomRepository)
    school_repo = providers.Factory(DjangoSchoolRepository)
    students_repo = providers.Factory(StudentsRepository)

    # The Classroom containers
    classroom_register_use_case = providers.Factory(
        RegisterClassroomUsercase,
        classroom_repo=classroom_repo,
        school_repo=school_repo,
    )

    classroom_response_use_case = providers.Factory(
        ResponseClassroomUseCase, classroom_repo=classroom_repo
    )

    classroom_update_use_case = providers.Factory(
        ClassroomUpdateUseCase,
        classroom_repo=classroom_repo,
        school_repo=school_repo,
    )

    classroom_list_use_case = providers.Factory(
        ListClassroomUseCase, classroom_repo=classroom_repo
    )

    classroom_deactive_use_case = providers.Factory(
        DeactiveClassroomUseCase, classroom_repo=classroom_repo
    )

    # The Students containers
    student_register_use_case = providers.Factory(
        RegisterStudentsUseCase,
        students_repo=students_repo,
        classroom_repo=classroom_repo,
    )

    students_response_use_case = providers.Factory(
        ResponseStudentsUseCase, students_repo=students_repo
    )

    students_update_use_case = providers.Factory(
        StudentsUpdateUseCase, students_repo=students_repo
    )

    students_list_use_case = providers.Factory(
        ListStudentsUseCase, students_repo=students_repo
    )

    students_deactive_use_case = providers.Factory(
        DeactiveStudentsUseCase, students_repo=students_repo
    )
