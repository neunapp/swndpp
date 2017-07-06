# django
from django.conf.urls import url

# local
from . import viewsets


urlpatterns = [
    #recuperar movimientos de guia
    url(
        r'^api/pagos/movimientos/(?P<guide>[-\w]+)/$',
        viewsets.MovimientosGuideViewSet.as_view({'get': 'list'}),
        name='pagos-movimientos'
    ),
]
