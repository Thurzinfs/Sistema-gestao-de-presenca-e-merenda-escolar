from typing import List
from uuid import UUID
from ninja import Router
from django.db.transaction import atomic
from app.canteen.api.dependencies import CanteenContainer
from app.canteen.api.schemas import (
    DailyMenuIn,
    DailyMenuOut,
    DailyMenuUpdate,
    LeftouversLunchIn,
    LeftouversLunchOut,
    LeftouversLunchUpdate,
    IngredientIn,
    IngredientOut
)
from datetime import date as Date

router = Router()
leftouverslunch_router = Router()
ingredients_router = Router()

canteen_container = CanteenContainer()


@router.post('/', response={201: DailyMenuOut})
@atomic
def register_daily_menu(request, data: DailyMenuIn, ingredients: List[IngredientIn]):
    use_case = canteen_container.register_daily_menu_use_case()
    dto = data.to_dto()
    response = use_case.execute(dto, [ingredient.to_dto() for ingredient in ingredients])
    return 201, DailyMenuOut.from_domain(response)

@router.get('/{id}', response={200: DailyMenuOut})
def view_by_id(request, id: UUID):
    use_case = canteen_container.daily_menu_return_with_id_use_case()
    response = use_case.execute(id)
    return 200, DailyMenuOut.from_domain(response)


@router.get('/', response={200: DailyMenuOut})
def view_daily_menu(request, date: Date):
    use_case = canteen_container.daily_menu_return_use_case()
    response = use_case.execute(date)
    return 200, DailyMenuOut.from_domain(response)


@router.get('/date_range/', response={200: List[DailyMenuOut]})
def view_with_date_range(request, from_date: Date, to_date: Date):
    use_case = canteen_container.daily_menu_return_with_date_range_use_case()
    entities = use_case.execute(from_date, to_date)
    return 200, [DailyMenuOut.from_domain(entity) for entity in entities]


@router.patch('/{id}', response={200: DailyMenuOut})
@atomic
def update_daily_menu(request, id: UUID, data: DailyMenuUpdate):
    use_case = canteen_container.daily_menu_update_use_case()
    dto = data.to_dto()
    response = use_case.execute(id, dto)
    return 200, DailyMenuOut.from_domain(response)


@leftouverslunch_router.post('/', response={201: LeftouversLunchOut})
@atomic
def register_leftouvers_lunch(request, data: LeftouversLunchIn):
    use_case = canteen_container.leftouvers_lunch_register_use_case()
    dto = data.to_dto()
    response = use_case.execute(dto)
    return 201, LeftouversLunchOut.from_domain(response)


@leftouverslunch_router.get('/{id}', response={200: LeftouversLunchOut})
def view_leftouvers_by_id(request, id: UUID):
    use_case = (
        canteen_container.leftouvers_lunch_return_with_id_use_case()
    )
    response = use_case.execute(id)
    return 200, LeftouversLunchOut.from_domain(response)


@leftouverslunch_router.get(
    '/month/{month}', response={200: LeftouversLunchOut}
)
def view_leftouvers_by_month(request, month: int):
    use_case = (
        canteen_container.leftouvers_lunch_return_with_month_use_case()
    )
    response = use_case.execute(month)
    return 200, LeftouversLunchOut.from_domain(response)


@leftouverslunch_router.patch('/{id}', response={200: LeftouversLunchOut})
@atomic
def update_leftouvers_lunch(request, id: UUID, data: LeftouversLunchUpdate):
    use_case = canteen_container.leftouvers_lunch_update_use_case()
    dto = data.to_dto()
    response = use_case.execute(id, dto)
    return 200, LeftouversLunchOut.from_domain(response)

@ingredients_router.get('/by-menu', response={200: List[IngredientOut]})
def view_by_daily_menu(request, daily_menu_id: UUID):
    use_case = canteen_container.ingredients_return_with_daily_menu_use_case()

    response = use_case.execute(daily_menu_id)
    return 200, [IngredientOut.from_domain(entity) for entity in response]

@ingredients_router.get('/{id}', response={200: IngredientOut})
def view_ingredient(request, id: UUID):
    use_case = canteen_container.ingredients_return_with_id_use_case()

    response = use_case.execute(id)
    return 200, IngredientOut.from_domain(response)
