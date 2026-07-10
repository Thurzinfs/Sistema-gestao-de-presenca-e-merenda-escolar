from dependency_injector import containers, providers

from app.school.application.use_cases import DeactiveSchoolUseCase, RegisterSchoolUseCase, ResponseSchoolUseCase, UpdateSchoolUseCase
from app.school.infrastructure.repository import DjangoSchoolRepository


class SchoolContainer(containers.DeclarativeContainer):
    school_repo = providers.Factory(DjangoSchoolRepository)

    register_school_use_case = providers.Factory(
        RegisterSchoolUseCase,
        school_repo=school_repo
    )

    response_school_use_case = providers.Factory(
        ResponseSchoolUseCase,
        school_repo=school_repo
    )

    update_school_use_case = providers.Factory(
        UpdateSchoolUseCase,
        school_repo=school_repo
    )

    deactive_school_use_case = providers.Factory(
        DeactiveSchoolUseCase,
        school_repo=school_repo
    )
