import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, View

from VotacionesUca.forms import DataForm

from UsuarioUca.models import UsuarioUca

# Create your views here.


def home(request):
    return render(request,'VotacionesUca/home.html')

def crearVotacion(request):
    return render(request,'VotacionesUca/CrearVotacion.html')

#Subir y guardar .CSV
class DataView(FormView):
    template_name = 'VotacionesUca/base.html'
    form_class = DataForm
    success_url = '/upload/'

    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)

#Descargar .CSV
class CSVFileView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('users.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('nif', 'email', 'firstname', 'lastname', 'password', 'isstaff', 'issuperuser', 'isactive')
        data = UsuarioUca.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writerheader()
        for row in data:
            writer.writerow(row)

        return response

