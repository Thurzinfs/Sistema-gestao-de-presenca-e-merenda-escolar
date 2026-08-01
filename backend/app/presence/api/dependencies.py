from dependency_injector import containers, providers

from app.presence.application.use_cases import (
    FrequencyListAll, 
    FrequencyRegisterUseCase, 
    ReadingAllUseCase, 
    ReadingRegisterUseCase, 
    ReadingResponseUseCase, 
    RegisterSnackRegisterUseCase,  
    ResponseAllRegisterSnackUseCase, 
    ResponseRegisterSnackByDateUseCase, 
    ResponseRegisterSnackByMomentUseCase, 
    ResponseRegisterSnackByTypeSnackUseCase
)

from app.presence.infrastructure.repository import ReadingRepository, RegisterSnackRepository

class PresenceContainer(containers.DeclarativeContainer):
    reading_repo = providers.Factory(ReadingRepository)

    register_readign_use_case = providers.Factory(
        ReadingRegisterUseCase, reading_repo = reading_repo
    )

    list_all_reading_use_case = providers.Factory(
        ReadingRegisterUseCase, reading_repo = reading_repo
    )

    response_reading_use_case = providers.Factory(
        ReadingResponseUseCase, reading_repo = reading_repo
    )

    frequency_repo = providers.Factory(ReadingRepository)
    register_frequency_use_case = providers.Factory(
        FrequencyRegisterUseCase, frequency_repo = frequency_repo
    )

    list_frequency_all_use_case = providers.Factory(
        FrequencyListAll, frequency_repo = frequency_repo
    )

    register_snack_repo = providers.Factory(RegisterSnackRepository)

    register_register_snack_use_case = providers.Factory(
        RegisterSnackRegisterUseCase,
        register_snack_repo = register_snack_repo
    )

    response_register_snack_all_use_case = providers.Factory(
        ResponseAllRegisterSnackUseCase,
        register_snack_repo = register_snack_repo
    )

    response_register_snack_by_date = providers.Factory(
        ResponseRegisterSnackByDateUseCase, register_snack_repo
    )

    response_register_snack_by_moment = providers.Factory(
        ResponseRegisterSnackByMomentUseCase, register_snack_repo
    )

    response_register_snack_by_type_snack = providers.Factory(
        ResponseRegisterSnackByTypeSnackUseCase, register_snack_repo
    )


