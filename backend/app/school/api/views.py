from typing import List
from uuid import UUID

from ninja import Router

from app.school.api.bearer import AuthBearer
from app.school.api.dependencies import SchoolContainer
from app.school.api.schemas import LoginIn, LoginOut, ManagerIn, ManagerOut, ManagerUpdate, SchoolIn, SchoolOut, SchoolUpdate

from django.db.transaction import atomic

router_school = Router()

router_manager = Router()

router_auth = Router()

container = SchoolContainer()


@router_school.post('/', response={201: SchoolOut})
@atomic
def register_school(request, data: SchoolIn):
    dto = data.to_dto()

    use_case = container.register_school_use_case()

    school = use_case.execute(dto)

    return SchoolOut.from_domain(school)

@router_school.get('/list/actives', response={200: List[SchoolOut]})
def list_schools(request):
    use_case = container.list_schools_use_case()

    schools = use_case.execute()

    return 200, [
        SchoolOut.from_domain(school)
        for school in schools
    ]

@router_school.get('/{id}', response={200: SchoolOut})
def response_school(request, id: UUID):
    use_case = container.response_school_use_case()

    school = use_case.execute(id)

    return SchoolOut.from_domain(school)


@router_school.patch('/{id}', response={200: SchoolOut})
@atomic
def update_school(request, id: UUID, data: SchoolUpdate):
    dto = data.to_dto()

    use_case = container.update_school_use_case()

    school = use_case.execute(id, dto)

    return SchoolOut.from_domain(school)


@router_school.delete('/{id}', response={200: SchoolOut})
@atomic
def deactive_school(request, id: UUID):
    use_case = container.deactive_school_use_case()

    school = use_case.execute(id)

    return SchoolOut.from_domain(school)


@router_manager.post('/', response={201: ManagerOut})
@atomic
def register_manager(request, data: ManagerIn):
    dto = data.to_dto()

    use_case = container.register_manager_use_case()

    manager = use_case.execute(dto)

    return ManagerOut.from_domain(manager)


@router_manager.get('/{id}', response={200: ManagerOut})
def response_manager(request, id: UUID):
    use_case = container.response_manager_use_case()

    manager = use_case.execute(id)

    return ManagerOut.from_domain(manager)


@router_manager.patch('/{id}', response={200: ManagerOut})
@atomic
def update_manager(request, id: UUID, data: ManagerUpdate):
    dto = data.to_dto()

    use_case = container.update_manager_use_case()

    manager = use_case.execute(id, dto)
    return ManagerOut.from_domain(manager)


@router_manager.delete('/{id}', response={200: ManagerOut})
@atomic
def deactive_manager(request, id: UUID):
    use_case = container.deactive_manager_use_case()

    manager = use_case.execute(id)

    return ManagerOut.from_domain(manager)

@router_auth.post('/', response={201: LoginOut})
def login(request, data: LoginIn):
    dto = data.to_dto()

    use_case = container.login_use_case()

    login = use_case.execute(dto)

    return 201, LoginOut.from_domain(login)

@router_auth.get('/me', response={200: ManagerOut}, auth=AuthBearer())
def request_me(request):
    return ManagerOut.from_domain(request.auth)
