from ninja import NinjaAPI

from app.school.api.views import router_school, router_manager, router_auth


app = NinjaAPI(
    title='Gestor de Presença e Merenda Escolar',
    version='0.1.0',
    docs_url='/docs/',
)

app.add_router('/school', router_school, tags=['School'])
app.add_router('/school/manager', router_manager, tags=['Manager'])
app.add_router('/auth', router_auth, tags=['Auth'])
