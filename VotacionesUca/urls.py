from django.contrib import admin
from django.urls import path, include
from .views import CrearVotacionView, VotacionView, VotacionComplejaView

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacion/<slug:pk>', VotacionView.as_view(), name="votacionsimple"),
    # path('votacionCompleja/', VotacionComplejaView.as_view(), name="votacioncompleja")
]
