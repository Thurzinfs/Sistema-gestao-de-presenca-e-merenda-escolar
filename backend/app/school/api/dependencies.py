from dependency_injector import containers, providers

from app.school.application.use_cases import (
    DeactiveManagerUseCase,
    DeactiveSchoolUseCase,
    RegisterManagerUseCase,
    RegisterSchoolUseCase,
    ResponseManagerByIDUseCase,
    ResponseSchoolUseCase,
    UpdateManagerUseCase,
    UpdateSchoolUseCase,
)
from app.school.infrastructure.repository import (
    DjangoManagerRepository,
    DjangoSchoolRepository,
)


class SchoolContainer(containers.DeclarativeContainer):
    school_repo = providers.Factory(DjangoSchoolRepository)

    register_school_use_case = providers.Factory(
        RegisterSchoolUseCase, school_repo=school_repo
    )

    response_school_use_case = providers.Factory(
        ResponseSchoolUseCase, school_repo=school_repo
    )

    update_school_use_case = providers.Factory(
        UpdateSchoolUseCase, school_repo=school_repo
    )

    deactive_school_use_case = providers.Factory(
        DeactiveSchoolUseCase, school_repo=school_repo
    )

    manager_repo = providers.Factory(DjangoManagerRepository)

    register_manager_use_case = providers.Factory(
        RegisterManagerUseCase, manager_repo=manager_repo
    )

    response_manager_use_case = providers.Factory(
        ResponseManagerByIDUseCase, manager_repo=manager_repo
    )

    update_manager_use_case = providers.Factory(
        UpdateManagerUseCase, manager_repo=manager_repo
    )

    deactive_manager_use_case = providers.Factory(
        DeactiveManagerUseCase, manager_repo=manager_repo
    )
