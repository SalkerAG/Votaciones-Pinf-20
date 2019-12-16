from django.views.generic import TemplateView
from .models import ProcesoElectoral,Opciones,Pregunta,Votacione,Eleccion
from .forms import VotacioneForm
from django.shortcuts import render,redirect
import datetime

class CrearVotacionView(TemplateView):
    template_name='CrearVotacion.html'

    def get(self,request):
        form=VotacioneForm()
        post=Votacione.objects.all()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=VotacioneForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()

            form=VotacioneForm()
            return redirect('/crearVotacion/')

        args={'form':form}
        return render(request,self.template_name,args)
