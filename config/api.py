from ninja import NinjaAPI

from app.school.api.views import router_school, router_manager
from app.canteen.api.views import router as router_canteen
from app.presence.api.views import reading_router
from app.presence.api.views import frequency_router
from app.presence.api.views import register_snack_router
from app.school.api.views import router_school, router_manager, router_auth

from app.canteen.api.views import (
    leftouverslunch_router,
    router as router_canteen,
    ingredients_router
)


from app.academic.api.views import route_classroom,route_students

app = NinjaAPI(
    title='Gestor de Presença e Merenda Escolar',
    version='0.1.0',
    docs_url='/docs/',
)

app.add_router('/auth', router_auth, tags=['Auth'])
app.add_router('/school', router_school, tags=['School'])
app.add_router('/school/manager', router_manager, tags=['Manager'])
app.add_router('/academic/classroom', route_classroom, tags=['Classroom'])
app.add_router('/academic/students', route_students, tags=['Students'])
app.add_router('/canteen', router_canteen, tags=['Canteen'])
app.add_router('/ingredients', ingredients_router, tags=['Ingredient'])
app.add_router('/presence/readings', reading_router, tags=['Readings'])
app.add_router('/presence/frequency', frequency_router, tags=['Frequency'])
app.add_router('/presence/registerSnack', register_snack_router, tags=['Register snack'])
app.add_router(
    '/canteen/leftouvers', leftouverslunch_router, tags=['Leftouvers Lunch']
)

@app.get('/health/', tags=['Health'])
def request_health(request):
    return 200