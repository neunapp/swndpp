from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url para home de la aplicacion
    url(
        r'^guia-registrar/$',
        views.GuideRegisterView.as_view(),
        name='add-guide'
    ),
    #url para listar diarios
    url(
        r'^magazine-listar/$',
        views.MagazineListView.as_view(),
        name='list-magazine'
    ),
    #url para agregar diarios
    url(
        r'^magazine-add/$',
        views.MagazineCreate.as_view(),
        name='add-magazine'
    ),
    #url para agregar productos
    url(
        r'^prod-add/$',
        views.ProductCreate.as_view(),
        name='add-prod'
    ),
    #url para listar diarios
    url(
        r'^lista-dias-diarios/(?P<pk>\d+)/(?P<tipo>\d+)/$',
        views.DaysTemplateView.as_view(),
        name='list_day-magazine'
    ),




    #rest de aplicacion recepcion
    url(r'^', include('applications.recepcion.url_services', namespace="recepcion_servis_url")),
]
