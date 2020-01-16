from time import timezone

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, forms, formset_factory
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin, UpdateView
from django.urls import reverse
from django.views.generic import TemplateView, FormView, CreateView, DetailView
from django.views.generic.list import ListView
from import_export import resources
from django.http import HttpRequest as request, HttpResponseRedirect, HttpResponse
from odf import form

from UsuarioUca.admin import UsuarioUcaResource
from UsuarioUca.import_export_views import ImportView
from UsuarioUca.models import UsuarioUca
from VotacionesUca.admin import CensoResource
from .models import ProcesoElectoral, Pregunta, Votacion, Eleccion, Censo, \
    UsuarioVotacion, OpcionesCompleja, UsuarioEleccion, Personas
from .forms import VotacionForm, PreguntaForm, createCensoForm, PreguntaFormVotacion, \
    realizarVotacionForm, OpcionesComplejaForm, realizarVotacionComplejaForm, EleccionForm, realizarEleccionForm, \
    PersonaForm, ListaVotacionForm, ListaEleccionForm, ListaCensoForm, realizarEleccionFormGrupos, \
    EleccionCensoFormUpdate, EleccionUpdateForm
from django.shortcuts import render, redirect
import datetime
import csv
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy


class CrearPreguntaViewCenso(LoginRequiredMixin, BSModalCreateView):
    form_class = PreguntaForm
    template_name = "CrearPregunta.html"
    success_message = 'Exito: Pregunta creada.'
    success_url = reverse_lazy('censo_create')


class CrearPreguntaViewRealizarVotacion(LoginRequiredMixin, BSModalCreateView):
    form_class = PreguntaForm
    template_name = "CrearPregunta.html"
    success_message = 'Exito: Pregunta creada.'
    success_url = reverse_lazy('realizarvotacion')


class CrearPreguntaViewVotacion(LoginRequiredMixin, BSModalCreateView):
    form_class = PreguntaForm
    template_name = "CrearPregunta.html"
    success_message = 'Exito: Pregunta creada.'
    success_url = reverse_lazy('crearvotacion')


class CrearCensoVotacionView(LoginRequiredMixin, CreateView):
    model = Censo
    form_class = createCensoForm
    template_name = 'censoVotacion.html'

    def get_success_url(self):
        return reverse('censo-detail', kwargs={"pk": self.object.pk})


class CrearCensoEleccionView(LoginRequiredMixin, CreateView):
    model = Censo
    form_class = createCensoForm
    template_name = 'censoEleccion.html'

    def get_success_url(self):
        return reverse('censo-detail', kwargs={"pk": self.object.pk})


class CensoDetailView(LoginRequiredMixin, DetailView):
    model = Censo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['users'] = self.object.usuario.all
        return context


class CensoExportView(LoginRequiredMixin, ImportView, resources.ModelResource):
    class Meta:
        model = UsuarioUca

    def get(self, queryset, *args, **kwargs):
        censo_id = kwargs.pop("pk")
        censo = Censo.objects.get(id=censo_id)
        users_censo = censo.usuario.all()
        for user in users_censo:
            user.nif = user.nif.replace("u", "")
            user.nif = user.nif[:2] + "*" + user.nif[5:]
        output = []
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Censo' + str(censo_id) + '.csv'
        writer = csv.writer(response)
        query_set = users_censo
        writer.writerow(['Nif'])
        for user in query_set:
            output.append([user])

        writer.writerows(output)
        return response


class CrearVotacionView(LoginRequiredMixin, CreateView):
    model = Votacion
    form_class = VotacionForm

    def get_success_url(self):
        return reverse('crearpreguntavotacion', kwargs={"pk": self.object.pk})


def load_preguntas(request):
    Votacion_id = request.GET.get('Votacion')
    preguntas = Pregunta.objects.filter(Votacion_id=Votacion_id).order_by('enunciado')
    return render(request, 'preguntas_list_options.html', {'preguntas': preguntas})


class CrearPregunta(LoginRequiredMixin, CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'CrearPregunta.html'

    def get_success_url(self):

        if self.object.tipo_votacion == "0":
            return reverse('home')
        else:
            return reverse('crearpreguntacompleja')


class CrearPreguntaVotacion(LoginRequiredMixin, FormMixin, DetailView, request):
    model = Votacion
    form_class = PreguntaFormVotacion
    template_name = "CrearPreguntaVotacion.html"

    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(CrearPreguntaVotacion, self).get_context_data(**kwargs)

        context['form'] = PreguntaFormVotacion(
            initial={'Votacion': self.object})
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        form = self.get_form()
        pregunta = Pregunta()

        pregunta.Votacion = self.object

        pregunta.enunciado = form.data['enunciado']
        pregunta.tipo_votacion = form.data['tipo_votacion']

        pregunta.save()
        if pregunta.tipo_votacion == '0':
            return HttpResponseRedirect('/')
        else:
            url = reverse('crearpreguntacompleja', kwargs={"pk": self.object.pregunta.pk})
            return HttpResponseRedirect(url)

    def form_valid(self, form):
        form.save()
        return super(CrearPreguntaVotacion, self).form_valid(form)


class CrearPreguntaComplejaView(LoginRequiredMixin, FormMixin, DetailView, request):
    model = Pregunta
    form_class = OpcionesComplejaForm
    template_name = "CrearVotacionCompleja.html"

    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(CrearPreguntaComplejaView, self).get_context_data(**kwargs)
        context['respuestas'] = OpcionesCompleja.objects.filter(Pregunta_id=kwargs['object'].id)

        context['form'] = OpcionesComplejaForm(
            initial={'Pregunta': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # print(self.object)
        form = self.get_form()
        oc = OpcionesCompleja()

        oc.Pregunta = self.object

        oc.respuesta = form.data['respuesta']

        if OpcionesCompleja.objects.filter(Pregunta_id=oc.Pregunta, respuesta=oc.respuesta).count() > 0:
            messages.error(request, "Respuesta ya introducida en la pregunta")
        else:
            oc.save()

        return HttpResponseRedirect(self.request.path_info)

    def form_valid(self, form):
        form.save()
        return super(CrearPreguntaComplejaView, self).form_valid(form)


class VotacionView(LoginRequiredMixin, FormMixin, DetailView, request):
    model = Votacion
    form_class = realizarVotacionForm
    template_name = "RealizarVotacion.html"

    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse('home')

    def render_to_response(self, context, **response_kwargs):
        votacion = Votacion.objects.get(pk=context['votacion'].id)
        if Censo.objects.filter(votacion_id=context['votacion'].id).exists():
            censo = Censo.objects.get(votacion_id=context['votacion'].id)
        else:
            url = reverse('home')
            return HttpResponseRedirect(url)
        if self.request.user not in censo.usuario.all():
            url = reverse('home')
            return HttpResponseRedirect(url)
        else:
            if UsuarioVotacion.objects.filter(user_id=self.request.user.id, Votacion_id=votacion.id).exists():
                if not votacion.voto_rectificable:
                    if votacion.es_consulta:
                        if Pregunta.objects.get(Votacion_id=votacion.id).tipo_votacion == '0':
                            url = reverse('estadisticasvotacionsimple', kwargs={'pk': votacion.id})
                            return HttpResponseRedirect(url)
                        else:
                            url = reverse('estadisticasvotacioncompleja', kwargs={'pk': votacion.id})
                            return HttpResponseRedirect(url)
                    else:
                        url = reverse('home')
                        return HttpResponseRedirect(url)
            return super(VotacionView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(VotacionView, self).get_context_data(**kwargs)

        if self.object.pregunta.tipo_votacion == '0':
            context['form'] = realizarVotacionForm(
                initial={'user': self.request.user, 'Votacion': self.object, 'Pregunta': self.object.pregunta})
            return context
        else:
            respuestasComplejas = OpcionesCompleja.objects.filter(Pregunta_id=self.object.pregunta.id)
            context['form'] = realizarVotacionComplejaForm(
                initial={'user': self.request.user, 'Votacion': self.object, 'Pregunta': self.object.pregunta,
                         'respuestas': respuestasComplejas})
            return context

    def post(self, request, *args, **kwargs):
        global seleccionprevia
        self.object = self.get_object()

        form = self.get_form()
        usuario_eleccion = UsuarioVotacion()
        listado_usuarios_votacion = Censo.objects.get(votacion_id=self.object.id)
        usuario_eleccion.user = self.request.user
        usuario_eleccion.Votacion = self.object
        usuario_eleccion.Pregunta = self.object.pregunta

        if usuario_eleccion.Pregunta.tipo_votacion == '1':
            usuario_eleccion.seleccion = form.data['respuesta']
        else:
            usuario_eleccion.seleccion = form.data['respuesta']

        if usuario_eleccion.user not in listado_usuarios_votacion.usuario.all():
            return HttpResponseRedirect('/errorVotacion')
        else:
            listado_usuarios = UsuarioVotacion.objects.filter(Votacion_id=self.object.id).all()
            listado_usuarios_votados = []
            for user in listado_usuarios:
                listado_usuarios_votados.append(user.user)
            if usuario_eleccion.user in listado_usuarios_votados:
                if self.object.pregunta.Votacion.voto_rectificable == False and self.object.pregunta.Votacion.es_consulta == True:
                    url = reverse('estadisticasvotacionsimple', kwargs={"pk": self.object.pk})
                    return HttpResponseRedirect(url)
                elif self.object.pregunta.Votacion.voto_rectificable == False and self.object.pregunta.Votacion.es_consulta == False:
                    return HttpResponseRedirect('/errorVotacionRectificable')
                else:
                    usuario_eleccion.save()
                    if usuario_eleccion.Votacion.es_consulta:
                        if usuario_eleccion.Pregunta.tipo_votacion == '0':
                            url = reverse('estadisticasvotacionsimple', kwargs={'pk': usuario_eleccion.Votacion.id})
                            return HttpResponseRedirect(url)
                        else:
                            url = reverse('estadisticasvotacioncompleja', kwargs={'pk': usuario_eleccion.Votacion.id})
                            return HttpResponseRedirect(url)
                    else:
                        return HttpResponseRedirect('/')
            else:
                usuario_eleccion.save()
                if usuario_eleccion.Votacion.es_consulta:
                    if usuario_eleccion.Pregunta.tipo_votacion == '0':
                        url = reverse('estadisticasvotacionsimple', kwargs={'pk': usuario_eleccion.Votacion.id})
                        return HttpResponseRedirect(url)
                    else:
                        url = reverse('estadisticasvotacioncompleja', kwargs={'pk': usuario_eleccion.Votacion.id})
                        return HttpResponseRedirect(url)
                else:
                    return HttpResponseRedirect('/')


class EleccionView(LoginRequiredMixin, FormMixin, DetailView, request):
    model = Eleccion
    form_class = realizarEleccionForm
    template_name = "RealizarEleccion.html"

    success_url = reverse_lazy('home')

    def get_form(self, form_class=realizarEleccionForm):
        form = super().get_form(form_class=self.form_class)
        form.fields['seleccion'].queryset = Personas.objects.all()

        return form

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse('home')

    def render_to_response(self, context, **response_kwargs):
        eleccion = Eleccion.objects.get(pk=context['eleccion'].id)
        if Censo.objects.filter(eleccion_id=context['eleccion'].id).exists():
            censoeleccion = Censo.objects.get(eleccion_id=context['eleccion'].id)
        else:
            url = reverse('home')
            return HttpResponseRedirect(url)
        if self.request.user not in censoeleccion.usuario.all():
            url = reverse('home')
            return HttpResponseRedirect(url)
        else:
            if UsuarioEleccion.objects.filter(user_id=self.request.user.id, Eleccion_id=eleccion.id).exists():
                if eleccion.es_consulta:

                    url = reverse('estadisticaseleccion', kwargs={'pk': eleccion.id})
                    return HttpResponseRedirect(url)

                else:
                    url = reverse('home')
                    return HttpResponseRedirect(url)
            return super(EleccionView, self).render_to_response(context, **response_kwargs)



    def get_context_data(self, **kwargs):

        context = super(EleccionView, self).get_context_data(**kwargs)
        cosas = self

        if self.object.tipo_eleccion == '1':
            seleccion = Personas.objects.filter(Eleccion_id=self.object.id)

            context['form'] = realizarEleccionForm(
                initial={'user': self.request.user, 'Eleccion': self.object, 'seleccion': seleccion})
            return context

        else:
            seleccion = Personas.objects.filter(Eleccion_id=self.object.id)
            context['form'] = realizarEleccionFormGrupos(id=self.object.id)

            return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        usuario_eleccion = UsuarioEleccion()

        listado_usuarios_votacion = Censo.objects.get(eleccion_id=self.object.id)

        usuario_eleccion.user = self.request.user
        usuario_eleccion.Eleccion = self.object

        usuario_eleccion.seleccion = request.POST.getlist('seleccion')

        if usuario_eleccion.user not in listado_usuarios_votacion.usuario.all():
            return HttpResponseRedirect('/errorVotacion')
        else:

            pass

        # listado_usuarios = UsuarioEleccion.objects.filter(Eleccion_id=self.object.id).all()
        # listado_usuarios_votados = []
        # for user in listado_usuarios:
        #     listado_usuarios_votados.append(user.user)
        #     if usuario_eleccion.user in listado_usuarios_votados:
        #         if self.object.es_consulta == True:
        #
        #             url = reverse('estadisticaseleccion', kwargs={"pk": self.object.pk})
        #             return HttpResponseRedirect(url)
        #
        #         elif self.object.es_consulta == False:
        #             return HttpResponseRedirect('/errorVotacionRectificable')
        #         else:
        #             usuario_eleccion.save()
        #             if usuario_eleccion.Eleccion.es_consulta:
        #                     url = reverse('estadisticasvotacioncompleja', kwargs={'pk': usuario_eleccion.Votacion.id})
        #                     return HttpResponseRedirect(url)
        #     else:
        #         return HttpResponseRedirect('/')

        usuario_eleccion.save()

        qss = Censo.objects.all().values_list('usuario', flat=True)

        if qss.filter(usuario=self.request.user).exists():

            usuario_eleccion.save()
        else:
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

    def form_valid(self, form):
        form.save()
        return super(EleccionView, self).form_valid(form)


class VotacionComplejaView(LoginRequiredMixin, FormView):
    template_name = 'VotacionCompleja.html'
    success_url = '/votacionCompleja/'
    form_class = VotacionForm

    def form_valid(self, form):
        return super().form_valid(form)


class ListaVotacionesView(LoginRequiredMixin, ListView):
    model = Votacion
    form_class = ListaVotacionForm
    paginate_by = 100  # if pagination is desired
    template_name = "ListaVotaciones.html"

    def get_queryset(self):
        votaciones_user = []
        if not self.request.user.is_superuser:
            censos_user = Censo.objects.filter(usuario=self.request.user).values_list('votacion_id', flat=True)
            if Censo.objects.filter(usuario=self.request.user).exists():
                votaciones_user = Votacion.objects.filter(id__in=censos_user)
            else:
                Votacion.objects.none()
            return votaciones_user
        else:
            return Votacion.objects.filter()

    def get_success_url(self):
        return reverse('votacion', kwargs={"pk": self.object.pk})


class ListaEleccionesView(LoginRequiredMixin, ListView):
    model = Eleccion
    form_class = ListaEleccionForm
    paginate_by = 100  # if pagination is desired
    template_name = "ListaElecciones.html"

    def get_queryset(self):
        elecciones_user = []
        if not self.request.user.is_superuser:
            censos_user = Censo.objects.filter(usuario=self.request.user).values_list('eleccion_id', flat=True)
            if Censo.objects.filter(usuario=self.request.user).exists():
                elecciones_user = Eleccion.objects.filter(id__in=censos_user)
            else:
                Eleccion.objects.none()
            return elecciones_user
        else:
            return Eleccion.objects.filter()

    def get_success_url(self):
        return reverse('eleccion', kwargs={"pk": self.object.pk})


class ListaCensosView(LoginRequiredMixin, ListView):
    model = Censo
    paginate_by = 100  # if pagination is desired
    template_name = "ListaCensos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        return context


class CrearEleccionView(LoginRequiredMixin, CreateView):
    model = Eleccion
    form_class = EleccionForm

    def get_success_url(self):
        return reverse('crearpersona', kwargs={"pk": self.object.pk})


class CrearPersona(LoginRequiredMixin, FormMixin, DetailView, request):
    model = Eleccion
    form_class = PersonaForm
    template_name = "personas_form.html"

    success_url = reverse_lazy('home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse('home')

    def people(self):
        return Personas.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CrearPersona, self).get_context_data(**kwargs)
        context['personas'] = Personas.objects.filter(Eleccion_id=kwargs['object'].id)
        context['form'] = PersonaForm(
            initial={'Eleccion': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        per = Personas()

        per.Eleccion = self.object

        per.nombre = form.data['nombre']

        maxcandidatos = per.Eleccion.max_candidatos
        maxvacantes = per.Eleccion.max_vacantes
        res = int(maxvacantes * maxcandidatos)

        print(res)

        if Personas.objects.filter(Eleccion_id=per.Eleccion, nombre=per.nombre).count() > 0:
            messages.error(request, "Nombre ya introducido en la elección")

        elif not Personas.objects.filter(Eleccion_id=per.Eleccion).count() > maxcandidatos - 1:

            per.save()


        else:

            messages.error(request, "Límite de candidatos posibles superado")

        if per.Eleccion.tipo_eleccion == '0':

            contador = (Personas.objects.filter(Eleccion_id=per.Eleccion_id).count())
            if contador > res:
                messages.error(request, "Límite de candidatos del grupo superado")

            else:
                per.save()

        return HttpResponseRedirect(self.request.path_info)

    def form_valid(self, form):
        form.save()
        return super(CrearPersona, self).form_valid(form)


class ErrorVotacionView(LoginRequiredMixin, TemplateView):
    template_name = 'ErrorVotacion.html'


class ErrorVotacionRectificableView(LoginRequiredMixin, TemplateView):
    template_name = 'ErrorVotacionRectificable.html'


class ExitoCensoVotacionView(LoginRequiredMixin, TemplateView):
    template_name = 'ErrorVotacion.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')


class VotacionUpdate(LoginRequiredMixin, UpdateView):
    model = Votacion
    form_class = VotacionForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('votacion_edit', kwargs={'pk': self.object.pk})


def erase_request1(request, pk):
    Votacion.objects.filter(id=pk).delete()
    return redirect('listavotaciones')


class EleccionUpdate(LoginRequiredMixin, UpdateView):
    model = Eleccion
    form_class = EleccionUpdateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('eleccion_edit', kwargs={'pk': self.object.pk})


def erase_persona(request, pk):
    persona = Personas.objects.get(id=pk)
    id = persona.Eleccion_id
    Personas.objects.filter(id=pk).delete()
    return redirect('crearpersona', pk=id)


def erase_respuesta(request, pk):
    respuesta = OpcionesCompleja.objects.get(id=pk)
    id = respuesta.Pregunta_id
    OpcionesCompleja.objects.filter(id=pk).delete()
    return redirect('crearpreguntacompleja', pk=id)


def erase_request2(request, pk):
    Eleccion.objects.filter(id=pk).delete()
    return redirect('listaelecciones')


class CensoEleccionUpdate(LoginRequiredMixin, UpdateView):
    model = Censo
    form_class = EleccionCensoFormUpdate
    template_name_suffix = '_eleccion_update_form'

    def get_success_url(self):
        return reverse('censo_eleccion_update', kwargs={'pk': self.object.pk})


class CensoUpdate(LoginRequiredMixin, UpdateView):
    model = Censo
    form_class = ListaCensoForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('censo_edit', kwargs={'pk': self.object.pk})


def erase_request3(request, pk):
    Censo.objects.filter(id=pk).delete()
    return redirect('listacensos')


class EstadisticasVotacionSimpleView(LoginRequiredMixin, DetailView):
    template_name = "votacionSimpleResultados.html"
    model = Votacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['censo'] = Censo.objects.get(pk=context['votacion'].votacion.censo.pk)
        context['usuariosCenso'] = context['censo'].usuario.all().count()
        context['total'] = 0
        context['si'] = 0
        context['no'] = 0
        context['abstencion'] = 0
        context['resultado'] = UsuarioVotacion.objects.filter(Votacion_id=context['votacion'].id)
        for resultado in context['resultado']:
            context['total'] += 1
            if resultado.seleccion == 'Si':
                context['si'] += 1
            else:
                if resultado.seleccion == 'No':
                    context['no'] += 1
                else:
                    context['abstencion'] += 1
        context['participacion'] = (context['total'] / context['usuariosCenso']) * 100
        context['abstencion'] = 100 - context['participacion']
        return context


class EstadisticasVotacionComplejaView(LoginRequiredMixin, DetailView):
    template_name = "votacionComplejaResultados.html"
    model = Votacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['censo'] = Censo.objects.get(pk=context['votacion'].votacion.censo.pk)
        context['usuariosCenso'] = context['censo'].usuario.all().count()
        context['total'] = 0
        fields = {}
        context['resultado'] = UsuarioVotacion.objects.filter(Votacion_id=context['votacion'].id)

        for resultado in context['resultado']:
            if resultado.seleccion not in fields:
                fields[resultado.seleccion] = 0

        for resultado in context['resultado']:
            context['total'] += 1
            fields[resultado.seleccion] += 1

        context['fields'] = fields
        context['participacion'] = (context['total'] / context['usuariosCenso']) * 100
        context['abstencion'] = 100 - context['participacion']
        return context


class EstadisticasEleccionView(LoginRequiredMixin, DetailView):
    template_name = "votacionEleccionesResultado.html"
    model = Eleccion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['censo'] = Censo.objects.get(eleccion_id=context['eleccion'].id)
        context['usuariosCenso'] = context['censo'].usuario.all().count()
        context['total'] = 0
        fields = {}
        context['resultado'] = UsuarioEleccion.objects.filter(Eleccion_id=context['eleccion'].id)

        for resultado in context['resultado']:
            if resultado.seleccion not in fields:
                fields[resultado.seleccion] = 0

        for resultado in context['resultado']:
            context['total'] += 1
            fields[resultado.seleccion] += 1

        context['fields'] = fields
        context['participacion'] = (context['total'] / context['usuariosCenso']) * 100
        context['abstencionporcentaje'] = (context['usuariosCenso'] - context['total']) / context['usuariosCenso'] * 100
        return context

class EstadisticasEleccionGrupoView(LoginRequiredMixin, DetailView):
    template_name = "votacionEleccionesGrupoResultado.html"
    model = Eleccion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['censo'] = Censo.objects.get(eleccion_id=context['eleccion'].id)
        context['usuariosCenso'] = context['censo'].usuario.all().count()
        context['total'] = 0
        fields = {}
        context['resultado'] = UsuarioEleccion.objects.filter(Eleccion_id=context['eleccion'].id)

        for resultado in context['resultado']:
            if resultado.seleccion not in fields:
                fields[resultado.seleccion] = 0

        for resultado in context['resultado']:
            context['total'] += 1
            fields[resultado.seleccion] += 1

        context['fields'] = fields
        context['participacion'] = (context['total'] / context['usuariosCenso']) * 100
        context['abstencionporcentaje'] = (context['usuariosCenso'] - context['total']) / context['usuariosCenso'] * 100
        return context
