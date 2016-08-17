from django.conf.urls import include, url

# from sapl.lexml.views import LexmlProvedorCrud, LexmlPublicadorCrud

from .views import add_oai_server, edit_oai_server

from .apps import AppConfig

app_name = AppConfig.name

urlpatterns = [
    # url(r'^sistema/lexml/provedor/',
    #     include(LexmlProvedorCrud.get_urls())),
    # url(r'^sistema/lexml/publicador/',
    #     include(LexmlPublicadorCrud.get_urls())),
    url(r'^sistema/lexml/OAI/add', add_oai_server),
    url(r'^sistema/lexml/OAI/edit', edit_oai_server)
]
