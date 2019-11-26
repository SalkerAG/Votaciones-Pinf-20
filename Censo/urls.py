from django.contrib import admin
from django.urls import path
from Censo.views import Censo
from .views import CensoCreate, CensoDetailView
from django.urls import reverse_lazy

urlpatterns = [
    path('censo/', CensoCreate.as_view(template_name="Censo/censo.html"), name="createCenso"),
    path('censo/<int:pk>', CensoDetailView.as_view(template_name="Censo/censo.html"), name="DetailCenso"),
    # path('censo/', Censo),# indicamos la ruta para acceder al censo y la vista Censo
    
    path('admin/', admin.site.urls),
]