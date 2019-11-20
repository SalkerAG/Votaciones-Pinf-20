from django.contrib import admin
from django.urls import path
from Censo.views import Censo, post

urlpatterns = [

    path('censo/', Censo),# indicamos la ruta para acceder al censo y la vista Censo
    path('censo/<id>',post),
    path('admin/', admin.site.urls),
]