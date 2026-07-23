from dependency_injector import providers, containers
from app.canteen.application.use_cases import (
    RegisterDailyMenuUseCase,
    ReturnDailyMenuUseCase,
    ReturnDailyMenuWithDateRangeUseCase,
    ReturnDailyMenuWithIdUseCase,
    UpdateDailyMenuUseCase,
)
from app.canteen.infrastructure.repository import DailyMenuRepository
from app.canteen.infrastructure.service import PickDatesService


class DailyMenuContainer(containers.DeclarativeContainer):
    daily_menu_repo = providers.Factory(DailyMenuRepository)
    pick_dates_service = providers.Factory(PickDatesService)

    register_daily_menu_use_case = providers.Factory(
        RegisterDailyMenuUseCase, daily_menu_repo=daily_menu_repo
    )

    return_daily_menu_use_case = providers.Factory(
        ReturnDailyMenuUseCase, daily_menu_repo=daily_menu_repo
    )

    update_daily_menu_use_case = providers.Factory(
        UpdateDailyMenuUseCase, daily_menu_repo=daily_menu_repo
    )

    return_with_date_range_use_case = providers.Factory(
        ReturnDailyMenuWithDateRangeUseCase, pick_dates_service=pick_dates_service
    )

    return_with_id_use_case = providers.Factory(
        ReturnDailyMenuWithIdUseCase, daily_menu_repo = daily_menu_repo
    )