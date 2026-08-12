from atexit import register
from datetime import datetime
from uuid import UUID

from ninja import Router

from app.presence.api.schema import FrequencyIn, FrequencyOut, ReadingIn, ReadingOut, RegisterSnackIn, RegisterSnackOut
from app.presence.api.dependencies import PresenceContainer
from app.presence.domain.role import MomentRole, SnackRole
from app.presence.infrastructure.models import Frequency

from django.db.transaction import atomic

from typing import List

reading_router = Router()

frequency_router = Router()

register_snack_router = Router()

container = PresenceContainer()


@reading_router.post('/', response=ReadingOut)
@atomic
def reading_register(request, data: ReadingIn):
    dto = data.to_dto()

    use_case = container.register_readign_use_case()

    reading = use_case.execute(dto)
 
    return ReadingOut.from_domain(reading)

@reading_router.get('/{id}', response=ReadingOut)
def response_reading(request, id: UUID):
    use_case = container.response_reading_use_case()

    reading = use_case.execute(id)
    
    return ReadingOut.from_domain(reading)

@reading_router.get('/', response=List[ReadingOut])
def reading_list_all(request):
    use_case = container.list_all_reading_use_case()

    readings = use_case.execute()

    return [ReadingOut.from_domain(reading) for reading in readings]


@frequency_router.post('/', response=FrequencyOut)
@atomic
def frequency_register(request, data: FrequencyIn):
    dto = data.to_dto()

    use_case = container.register_frequency_use_case()

    frequency = use_case.execute(dto)

    return FrequencyOut.from_domain(frequency)

@frequency_router.get('/', response=List[FrequencyOut])
def frequency_all(request):
    use_case = container.list_frequency_all_use_case()

    frequencysDTO = use_case.execute()
    return [ FrequencyOut.from_domain(frequency) for frequency in frequencysDTO]

@register_snack_router.post('/', response=RegisterSnackOut)
@atomic
def register_snack_register(request, data: RegisterSnackIn):
    dto = data.to_dto()

    use_case = container.register_register_snack_use_case()

    register_snack = use_case.execute(dto)

    return RegisterSnackOut.from_domain(register_snack)


@register_snack_router.get('/', response=List[RegisterSnackOut])
def response_all_snack_register(request):
    use_case = container.response_register_snack_all_use_case()

    register_snacks = use_case.execute()

    return [RegisterSnackOut.from_domain(register_snack) for register_snack in register_snacks]

@register_snack_router.get('/{date}', response=List[RegisterSnackOut])
def response_snack_register_by_date(request, date: datetime):
    use_case = container.response_register_snack_by_date()

    register_snacks = use_case.execute(date)

    return [RegisterSnackOut.from_domain(register_snack) for register_snack in register_snacks]

@register_snack_router.get('/moment/{moment}', response=List[RegisterSnackOut])
def response_all_snack_moment(request, moment: MomentRole):
    use_case = container.response_register_snack_by_moment()

    register_snacks = use_case.execute(moment)

    return [RegisterSnackOut.from_domain(register_snack) for register_snack in register_snacks]

@register_snack_router.get('/type/{type_snack}', response=List[RegisterSnackOut])
def response_all_snack_type_snack(request, type_snack: SnackRole):
    use_case = container.response_register_snack_by_type_snack()

    register_snacks = use_case.execute(type_snack)

    return [RegisterSnackOut.from_domain(register_snack) for register_snack in register_snacks]
