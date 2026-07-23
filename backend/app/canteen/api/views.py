from typing import List
from uuid import UUID
from ninja import Router
from django.db.transaction import atomic
from app.canteen.api.dependencies import DailyMenuContainer, LeftouversLunchContainer
from app.canteen.api.schemas import DailyMenuIn, DailyMenuOut, DailyMenuUpdate, LeftouversLunchIn, LeftouversLunchOut, LeftouversLunchUpdate
from datetime import date as Date

router = Router()
leftouverslunch_router = Router()

container = DailyMenuContainer
leftouverslunch_container = LeftouversLunchContainer


@router.post('/', response={201: DailyMenuOut})
@atomic
def register_daily_menu(request, data: DailyMenuIn):
    use_case = container.register_daily_menu_use_case()
    dto = data.to_dto()
    response = use_case.execute(dto)
    return 201, DailyMenuOut.from_domain(response)

@router.get('/{id}', response={200: DailyMenuOut})
def view_by_id(request, id: UUID):
    use_case = container.return_with_id_use_case()
    response = use_case.execute(id)
    return 200, DailyMenuOut.from_domain(response)

@router.get('/', response={200: DailyMenuOut})
def view_daily_menu(request, date: Date):
    use_case = container.return_daily_menu_use_case()
    response = use_case.execute(date)
    return 200, DailyMenuOut.from_domain(response)


@router.get('/date_range', response={200: List[DailyMenuOut]})
def view_with_date_range(request, from_date: Date, to_date: Date):
    use_case = container.return_with_date_range_use_case()
    entities = use_case.execute(from_date, to_date)
    return 200, [DailyMenuOut.from_domain(entity) for entity in entities]


@router.patch('/{id}', response={200: DailyMenuOut})
@atomic
def update_daily_menu(request, id: UUID, data: DailyMenuUpdate):
    use_case = container.update_daily_menu_use_case()
    dto = data.to_dto()
    response = use_case.execute(id, dto)
    return 200, DailyMenuOut.from_domain(response)

@leftouverslunch_router.post('/', response={201: LeftouversLunchOut})
def register_leftouvers_lunch(request, data: LeftouversLunchIn):
    use_case = leftouverslunch_container.register_leftouvers_lunch_use_case()
    dto = data.to_dto()
    response = use_case.execute(dto)
    return 201, LeftouversLunchOut.from_domain(response)

@leftouverslunch_router.get('/date', response={200: LeftouversLunchOut})
def view_by_date(request, date: Date):
    use_case = leftouverslunch_container.return_with_date_leftouvers_lunch_use_case()
    response = use_case.execute(date)
    return 200, LeftouversLunchOut.from_domain(response)