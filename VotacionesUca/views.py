from django.views.generic import ListView
from django.views.generic.edit import CreateView

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# Create your views here.
from .models import Votacione


class VotacioneCreateView(CreateView):
    models = Votacione
    fields = '__all__'

    def get_queryset(self):
        """Return the last five published questions."""
        return Votacione.objects.all()[:5]
