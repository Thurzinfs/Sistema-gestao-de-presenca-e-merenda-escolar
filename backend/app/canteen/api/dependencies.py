from dependency_injector import providers, containers
from app.canteen.application.use_cases import RegisterDailyMenuUseCase, ReturnDailyMenuUseCase, UpdateDailyMenuUseCase
from app.canteen.infrastructure.repository import DailyMenuRepository

class DailyMenuContainer(containers.DeclarativeContainer):
    daily_menu_repo = providers.Factory(DailyMenuRepository)

    register_daily_menu_use_case = providers.Factory(
        RegisterDailyMenuUseCase,
        daily_menu_repo = daily_menu_repo
    )

    return_daily_menu_use_case = providers.Factory(
        ReturnDailyMenuUseCase,
        daily_menu_repo = daily_menu_repo
    )

    update_daily_menu_use_case = providers.Factory(
        UpdateDailyMenuUseCase,
        daily_menu_repo = daily_menu_repo
    )