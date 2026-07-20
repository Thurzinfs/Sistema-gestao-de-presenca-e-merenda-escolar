from dependency_injector import containers, providers

from app.school.application.use_cases import DeactiveManagerUseCase, DeactiveSchoolUseCase, ListSchoolActivesUseCase, LoginUseCase, RegisterManagerUseCase, RegisterSchoolUseCase, ResponseManagerByIDUseCase, ResponseSchoolUseCase, UpdateManagerUseCase, UpdateSchoolUseCase
from app.school.infrastructure.repository import DjangoManagerRepository, DjangoRefreshTokenRepository, DjangoSchoolRepository
from app.school.infrastructure.services import HashService, TokenService


class SchoolContainer(containers.DeclarativeContainer):
    school_repo = providers.Factory(DjangoSchoolRepository)

    token_repo = providers.Factory(DjangoRefreshTokenRepository)

    token_service = providers.Factory(
        TokenService
    )

    hash_service = providers.Factory(
        HashService
    )

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
        RegisterManagerUseCase,
        manager_repo=manager_repo,
        hash_service=hash_service
    )

    response_manager_use_case = providers.Factory(
        ResponseManagerByIDUseCase, manager_repo=manager_repo
    )

    list_schools_use_case = providers.Factory(
        ListSchoolActivesUseCase,
        school_repo=school_repo
    )

    update_manager_use_case = providers.Factory(
        UpdateManagerUseCase, manager_repo=manager_repo
    )

    deactive_manager_use_case = providers.Factory(
        DeactiveManagerUseCase, manager_repo=manager_repo
    )

    login_use_case = providers.Factory(
        LoginUseCase,
        user_repo=manager_repo,
        token_repo=token_repo,
        token_service=token_service,
        hash_service=hash_service
    )
