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
    UpdateLeftouversLunchUseCase,
    ReturnIngredientWithIdUseCase,
    ReturnIngredientWithDailyMenuUseCase
)
from app.canteen.infrastructure.repository import (
    DailyMenuRepository,
    LeftouversLunchRepository,
    IngredientRepository
)
from app.canteen.infrastructure.service import (
    PickDatesService,
    VerifyLeftouverLunchExistsService,
)
from app.school.infrastructure.repository import (
    DjangoManagerRepository,
    DjangoSchoolRepository,
)


class CanteenContainer(containers.DeclarativeContainer):
    # dependencies of daily menu
    daily_menu_repo = providers.Factory(DailyMenuRepository)
    pick_dates_service = providers.Factory(PickDatesService)

    # dependencies of leftouvers lunch
    leftouvers_lunch_repo = providers.Factory(LeftouversLunchRepository)
    leftouvers_lunch_exists_service = providers.Factory(
        VerifyLeftouverLunchExistsService
    )
    manager_repo = providers.Factory(DjangoManagerRepository)
    school_repo = providers.Factory(DjangoSchoolRepository)

    # dependencies of ingredients
    ingredient_repo = providers.Factory(IngredientRepository)

    # daily menu use cases
    register_daily_menu_use_case = providers.Factory(
        RegisterDailyMenuUseCase, daily_menu_repo=daily_menu_repo, ingredient_repo = ingredient_repo
    )

    daily_menu_return_use_case = providers.Factory(
        ReturnDailyMenuUseCase, daily_menu_repo=daily_menu_repo
    )
    
    daily_menu_update_use_case = providers.Factory(
        UpdateDailyMenuUseCase, daily_menu_repo=daily_menu_repo
    )

    daily_menu_return_with_date_range_use_case = providers.Factory(
        ReturnDailyMenuWithDateRangeUseCase,
        pick_dates_service=pick_dates_service,
    )

    daily_menu_return_with_id_use_case = providers.Factory(
        ReturnDailyMenuWithIdUseCase, daily_menu_repo=daily_menu_repo
    )

    # leftouvers lunch use case
    leftouvers_lunch_register_use_case = providers.Factory(
        RegisterLeftouversLunchUseCase,
        leftouvers_lunch_repo=leftouvers_lunch_repo,
        leftouvers_lunch_exists_service=leftouvers_lunch_exists_service,
        manager_repo=manager_repo,
        school_repo=school_repo,
    )
    leftouvers_lunch_return_with_id_use_case = providers.Factory(
        ReturnLeftouversLunchWithIdUseCase,
        leftouvers_lunch_repo=leftouvers_lunch_repo,
    )
    leftouvers_lunch_return_with_month_use_case = providers.Factory(
        ReturnLeftouversLunchWithMonthUseCase,
        leftouvers_lunch_repo=leftouvers_lunch_repo,
    )
    leftouvers_lunch_update_use_case = providers.Factory(
        UpdateLeftouversLunchUseCase,
        leftouvers_lunch_repo=leftouvers_lunch_repo,
    )

    # ingredients use cases
    ingredients_return_with_id_use_case = providers.Factory(
        ReturnIngredientWithIdUseCase,
        ingredient_repo = ingredient_repo
    )
    ingredients_return_with_daily_menu_use_case = providers.Factory(
        ReturnIngredientWithDailyMenuUseCase,
        ingredient_repo = ingredient_repo
    )
