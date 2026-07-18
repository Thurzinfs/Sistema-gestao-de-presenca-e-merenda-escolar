from uuid import UUID
from ninja import Router
from django.db.transaction import atomic
from app.canteen.api.dependencies import DailyMenuContainer
from app.canteen.api.schemas import DailyMenuIn, DailyMenuOut, DailyMenuUpdate
from datetime import date as Date

router = Router()
container = DailyMenuContainer

@router.post('/', response={201: DailyMenuOut})
@atomic
def register_daily_menu(request, data: DailyMenuIn):
    use_case = container.register_daily_menu_use_case()
    dto = data.to_dto()
    response = use_case.execute(dto)
    return 201, DailyMenuOut.from_domain(response)

@router.get('/', response={200: DailyMenuOut})
def view_daily_menu(request, date: Date):
    use_case = container.return_daily_menu_use_case()
    response = use_case.execute(date)
    return 200, DailyMenuOut.from_domain(response)

@router.patch('/{id}', response={200: DailyMenuOut})
@atomic
def update_daily_menu(request, id: UUID, data: DailyMenuUpdate):
    use_case = container.update_daily_menu_use_case()
    dto = data.to_dto()
    response = use_case.execute(id, dto)
    return 200, DailyMenuOut.from_domain(response)