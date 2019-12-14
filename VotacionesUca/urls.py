from django.contrib import admin
from django.urls import path, include
from .views import CrearVotacionView

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
]
