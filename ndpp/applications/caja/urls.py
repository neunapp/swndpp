from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url para home de la aplicacion
    url(
        r'^registrar-pagos/$',
        views.PaymentRegister.as_view(),
        name='add-payment'
    ),
    #url para listar diarios



    #rest de aplicacion recepcion
    url(r'^', include('applications.caja.url_services', namespace="caja_servis_url")),
]
