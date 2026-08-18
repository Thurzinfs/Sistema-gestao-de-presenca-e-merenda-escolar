from typing import List
from uuid import UUID

from ninja import Router
from django.db.transaction import atomic

from app.academic.api.dependencies import AcademicContainer
from app.academic.api.schemas import (
    ClassroomIn,
    ClassroomOut,
    ClassroomUpdate,
    StudentsIn,
    StudentsOut,
    StudentsUpdate,
)
from app.academic.application import use_case


route_classroom = Router()
route_students = Router()
container = AcademicContainer()

# Routes from Classroom
@route_classroom.post('/', response={201: ClassroomOut})
@atomic
def register_classroom(request, data: ClassroomIn):
    dto = data.to_dto()
    use_case = container.classroom_register_use_case()
    response = use_case.execute(dto)
    return 201, ClassroomOut.from_domain(response)


@route_classroom.get('/list/actives', response={200: List[ClassroomOut]})
def list_active_classroom(request):
    use_case = container.classroom_list_use_case()
    classroom = use_case.execute(active=True)
    return 200, [ClassroomOut.from_domain(room) for room in classroom]


@route_classroom.get('/list/all', response={200: List[ClassroomOut]})
def list_all_classroom(request):
    use_case = container.classroom_list_use_case()
    classrooms = use_case.execute(active=None)
    return 200, [
        ClassroomOut.from_domain(classroom) for classroom in classrooms
    ]


@route_classroom.get('/{id}', response={200: ClassroomOut})
def response_classroom(request, id: UUID):
    use_case = container.classroom_response_use_case()
    classroom = use_case.execute(id)
    return 200, ClassroomOut.from_domain(classroom)


@route_classroom.patch('/{id}', response={201: ClassroomOut})
@atomic
def update_classroom(request, id: UUID, data: ClassroomUpdate):
    dto = data.to_dto()
    use_case = container.classroom_update_use_case()
    classroom = use_case.execute(id, dto)
    return 201, ClassroomOut.from_domain(classroom)


@route_classroom.delete('/{id}', response={200: ClassroomOut})
@atomic
def deactive_classroom(request, id: UUID):
    use_case = container.classroom_deactive_use_case()
    classroom = use_case.execute(id)
    return 200, ClassroomOut.from_domain(classroom)


# Routes from Students
@route_students.post('/', response={201: StudentsOut})
@atomic
def register_students(request, data: StudentsIn):
    dto = data.to_dto()
    use_case = container.student_register_use_case()
    students = use_case.execute(dto)
    return 201, StudentsOut.from_domain(students)


@route_students.get('/list/active', response={200: List[StudentsOut]})
def list_active_students(request):
    use_case = container.students_list_use_case()
    students = use_case.execute(active=True)
    return 200, [StudentsOut.from_domain(student) for student in students]


@route_students.get('/list/all', response={200: List[StudentsOut]})
def list_all_students(request):
    use_case = container.students_list_use_case()
    students = use_case.execute(active=None)
    return 200, [StudentsOut.from_domain(student) for student in students]


@route_students.get('/{id}', response={200: StudentsOut})
def response_students(request, id: UUID):
    use_case = container.students_response_use_case()
    students = use_case.execute(id)
    return 200, StudentsOut.from_domain(students)


@route_students.patch('/{id}', response={201: StudentsOut})
@atomic
def update_students(request, id: UUID, data: StudentsUpdate):
    dto = data.to_dto()
    use_case = container.students_update_use_case()
    students = use_case.execute(id, dto)
    return 201, StudentsOut.from_domain(students)


@route_students.delete('/{id}', response={200: StudentsOut})
@atomic
def deactive_students(request, id: UUID):
    use_case = container.students_deactive_use_case()
    students = use_case.execute(id)
    return 200, StudentsOut.from_domain(students)

@route_students.get('/qr_code/{qr_code}', response={200: StudentsOut})
def response_students_qrcode(request, qr_code: str):
    use_case = container.students_response_qr_code_use_case()
    students = use_case.execute(qr_code)
    return 200, StudentsOut.from_domain(students)
