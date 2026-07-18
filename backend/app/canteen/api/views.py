from ninja import Router
from django.db.transaction import atomic
from app.canteen.api.dependencies import DailyMenuContainer
from app.canteen.api.schemas import DailyMenuIn, DailyMenuOut

router = Router()
container = DailyMenuContainer

@router.post('/', response={201: DailyMenuOut})
@atomic
def register_daily_menu(request, data: DailyMenuIn):
    use_case = container.register_daily_menu_use_case()
    dto = data.to_dto()
    response = use_case.execute(dto)
    return 201, DailyMenuOut.from_domain(response)