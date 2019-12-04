from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import HomeView, ListaVotacionesView, CrearVotacionView, FAQView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name="home"),
    path('listavotaciones/', ListaVotacionesView.as_view(), name="listavotaciones"),
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('faq/', FAQView.as_view(), name="faq")
]