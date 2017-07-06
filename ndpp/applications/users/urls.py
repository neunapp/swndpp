from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^$',
        views.LogIn.as_view(),
        name='login'
    ),

    #url para home de la aplicacion
    url(
        r'^home/$',
        views.HomeView.as_view(),
        name='home'
    ),
]
