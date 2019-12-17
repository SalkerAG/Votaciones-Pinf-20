from django.contrib import admin
from django.urls import path, include
from .views import CrearVotacionView, VotacionSimpleView, VotacionComplejaView

urlpatterns = [
    path('crearVotacion/', CrearVotacionView.as_view(), name="crearvotacion"),
    path('votacionSimple/', VotacionSimpleView.as_view(), name="votacionsimple"),
    path('votacionCompleja/', VotacionComplejaView.as_view(), name="votacioncompleja")
]
