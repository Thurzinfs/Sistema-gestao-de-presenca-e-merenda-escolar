from dependency_injector import providers, containers
from app.canteen.application.use_cases import (
    RegisterDailyMenuUseCase,
    ReturnDailyMenuUseCase,
    ReturnDailyMenuWithDateRangeUseCase,
    ReturnDailyMenuWithIdUseCase,
    UpdateDailyMenuUseCase,
    RegisterLeftouversLunchUseCase,
    ReturnLeftouversLunchWithIdUseCase,
    ReturnLeftouversLunchWithMonthUseCase,
    UpdateLeftouversLunchUseCase
)
from app.canteen.infrastructure.repository import DailyMenuRepository, LeftouversLunchRepository
from app.canteen.infrastructure.service import PickDatesService, VerifyLeftouverLunchExistsService
from app.school.infrastructure.repository import DjangoManagerRepository, DjangoSchoolRepository


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

class LeftouversLunchContainer(containers.DeclarativeContainer):
    leftouvers_lunch_repo = providers.Factory(LeftouversLunchRepository)
    leftouvers_lunch_exists_service = providers.Factory(VerifyLeftouverLunchExistsService)
    manager_repo = providers.Factory(DjangoManagerRepository)
    school_repo = providers.Factory(DjangoSchoolRepository)

    register_leftouvers_lunch_use_case = providers.Factory(
        RegisterLeftouversLunchUseCase,
        leftouvers_lunch_repo=leftouvers_lunch_repo,
        leftouvers_lunch_exists_service=leftouvers_lunch_exists_service,
        manager_repo = manager_repo,
        school_repo = school_repo
    )
    return_with_id_leftouvers_lunch_use_case = providers.Factory(
        ReturnLeftouversLunchWithIdUseCase, leftouvers_lunch_repo=leftouvers_lunch_repo
    )
    return_with_month_leftouvers_lunch_use_case = providers.Factory(
        ReturnLeftouversLunchWithMonthUseCase, leftouvers_lunch_repo=leftouvers_lunch_repo
    )
    update_leftouvers_lunch_use_case = providers.Factory(
        UpdateLeftouversLunchUseCase, leftouvers_lunch_repo=leftouvers_lunch_repo
    )
