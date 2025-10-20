from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
from loguru import logger
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from chronos.tarefas.models import Tarefa, TarefaTempo, TarefaChecklist
from chronos.projetos.models import Projeto
from chronos.tarefas.model_forms import TarefaModelForm, TarefaChecklistForm, TarefaTempoForm
from chronos.tarefas.filters import ProjetoTarefaFilter
from chronos.reunioes.models import Reuniao


# Create your views here.
@login_required
def check_uncheck_checklist(request, checklist_id):
    projeto = TarefaChecklist.objects.filter(pk=checklist_id).get()
    projeto.concluido = not projeto.concluido
    projeto.save()
    return JsonResponse({
        'task_atualizada': True,
    })


@login_required
def tarefas_projeto(request, projeto_id):
    projeto = Projeto.objects.filter(pk=projeto_id).get()
    tarefas = Tarefa.objects.filter(projeto__pk=projeto_id).all()
    total_tempo = 0
    for tarefa in tarefas:
        total_tempo += tarefa.tempo_decorrido_segundos

    horas = int(total_tempo/3600)
    total_horas = total_tempo/3600
    media_hora = 0
    if projeto.valor > 0 and horas > 0:
        media_hora = float(projeto.valor) / horas

    return render(
        request,
        "projeto/tarefas_projeto.html",
        {
            "tarefas": tarefas,
            "projeto": projeto,
            "media_hora": media_hora,
            "total_horas": total_horas,
            "enum_status": Tarefa.StatusTarefa.choices,
        },
    )


@login_required
def tarefas_start(request, tarefa_id):
    tarefa = Tarefa.objects.filter(pk=tarefa_id).get()
    tarefa_tempo = TarefaTempo(
        tarefa=tarefa,
        inicio=datetime.now(),
        user=request.user
    )
    tarefa_tempo.save()
    url = request.GET.get("redirect", "tarefa-projeto-list")
    if url == "tarefa-kanban":
        return redirect(url)
    return redirect(url, projeto_id=tarefa.projeto.pk)


@login_required
def tarefas_pause(request, tarefa_id):
    tarefa = Tarefa.objects.filter(pk=tarefa_id).get()
    last_time = tarefa.tempos.last()
    last_time.fim = datetime.now()
    last_time.save()
    url = request.GET.get("redirect", "tarefa-projeto-list")
    if url == "tarefa-kanban":
        return redirect(url)
    return redirect(url, projeto_id=tarefa.projeto.pk)


class TarefasListView(LoginRequiredMixin, ListView):
    model = Tarefa


class TarefasCreateView(LoginRequiredMixin, CreateView):
    model = Tarefa
    form_class = TarefaModelForm

    def get_initial(self):
        initial = super().get_initial()
        projeto_id = self.request.GET.get("projeto_id")
        if projeto_id:
            projeto_default = Projeto.objects.get(pk=projeto_id)
            initial["projeto"] = projeto_default
        return initial

    def get_form(self):
        form = super().get_form()
        if form.initial.get('projeto'):
            logger.warning('projeto veio por parametro')
            form.fields['projeto'].widget = forms.widgets.HiddenInput()
        return form

    def get_success_url(self):
        context = self.get_context_data()
        projeto = context["form"].data.get("projeto")
        return reverse("tarefa-projeto-list", kwargs={"projeto_id": projeto})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["checklist_form"] = TarefaChecklistForm(
                self.request.POST, instance=self.object
            )
            context["tempo_form"] = TarefaTempoForm(
                self.request.POST, instance=self.object
            )
        else:
            context["checklist_form"] = TarefaChecklistForm(instance=self.object)
            context["tempo_form"] = TarefaTempoForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        checklist_form = context["checklist_form"]
        tempo_form = context["tempo_form"]
        if checklist_form.is_valid() and tempo_form.is_valid():
            self.object = form.save()  # Save the parent object first
            checklist_form.instance = (
                self.object
            )
            tempo_form.instance = (
                self.object
            )
            checklist_form.save()
            tempo_form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class TarefasUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarefa
    form_class = TarefaModelForm

    def get_initial(self):
        initial = super().get_initial()
        projeto_id = self.request.GET.get("projeto_id")
        if projeto_id:
            projeto_default = Projeto.objects.get(pk=projeto_id)
            initial["projeto"] = projeto_default
        return initial

    def get_form(self):
        form = super().get_form()
        if form.initial.get('projeto'):
            logger.warning('projeto veio por parametro')
            form.fields['projeto'].widget = forms.widgets.HiddenInput()
        return form

    def get_success_url(self):
        context = self.get_context_data()
        projeto = context["form"].data.get("projeto")
        url = self.request.GET.get("redirect", "tarefa-projeto-list")
        if url == "tarefa-kanban":
            return reverse(url)
        return reverse(url, kwargs={"projeto_id": projeto})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["checklist_form"] = TarefaChecklistForm(
                self.request.POST, instance=self.object
            )
            context["tempo_form"] = TarefaTempoForm(
                self.request.POST, instance=self.object
            )
        else:
            context["checklist_form"] = TarefaChecklistForm(instance=self.object)
            context["tempo_form"] = TarefaTempoForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        checklist_form = context["checklist_form"]
        tempo_form = context["tempo_form"]
        if checklist_form.is_valid() and tempo_form.is_valid():
            self.object = form.save()  # Save the parent object first
            checklist_form.instance = (
                self.object
            )
            tempo_form.instance = (
                self.object
            )
            checklist_form.save()
            tempo_form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, checklist_form=checklist_form, tempo_form=tempo_form))


class TarefasDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarefa
    success_url = reverse_lazy("tarefa-list")

    def get_success_url(self):
        projeto_id = self.request.GET.get("projeto_id")

        return reverse("tarefa-projeto-list", kwargs={"projeto_id": projeto_id})


class TarefasDetailView(LoginRequiredMixin, DetailView):
    model = Tarefa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enum_status"] = Tarefa.StatusTarefa.choices
        return context


class KanbanTarefasView(LoginRequiredMixin, TemplateView):
    template_name = "kanban/index.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tf = ProjetoTarefaFilter(self.request.GET, queryset=Tarefa.objects.all())
        tarefas_abertas = tf.qs.filter(
            status=Tarefa.StatusTarefa.ABERTA.value
        ).all()
        tarefas_em_andamento = tf.qs.filter(
            status=Tarefa.StatusTarefa.ANDAMENTO.value
        ).all()
        tarefas_bloqueadas = tf.qs.filter(
            status=Tarefa.StatusTarefa.BLOQUEADA.value
        ).all()
        tarefas_concluidas = tf.qs.filter(
            status=Tarefa.StatusTarefa.CONCLUIDA.value
        ).all()
        context["tarefas_abertas"] = tarefas_abertas
        context["tarefas_em_andamento"] = tarefas_em_andamento
        context["tarefas_bloqueadas"] = tarefas_bloqueadas
        context["tarefas_concluidas"] = tarefas_concluidas
        context["filter"] = tf
        return context


class CalendarTarefasView(LoginRequiredMixin, TemplateView):
    template_name = "calendar/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarefas = Tarefa.objects.exclude(
            status=Tarefa.StatusTarefa.CONCLUIDA.value
        ).all()
        reunioes = Reuniao.objects.all()
        context["tarefas"] = tarefas
        context["reunioes"] = reunioes
        eventos = []
        for tarefa in tarefas:
            if not tarefa.data_entrega:
                continue
            color = '#555555'
            if tarefa.status == Tarefa.StatusTarefa.ABERTA.value:
                color = '#007bff'
            elif tarefa.status == Tarefa.StatusTarefa.ANDAMENTO.value:
                color = '#ffc107'

            eventos.append(
                {
                    "title": tarefa.titulo,
                    "start": tarefa.data_entrega.strftime('%Y-%m-%d'),
                    "backgroundColor": color,
                    "borderColor": color,
                    "allDay": "true",
                }
            )

        for reuniao in reunioes:
            if not reuniao.inicio:
                continue
            if not reuniao.fim:
                continue
            color = 'red'

            eventos.append(
                {
                    "title": reuniao.nome,
                    "start": reuniao.inicio.strftime('%Y-%m-%d %H:%M:%S'),
                    "end": reuniao.fim.strftime('%Y-%m-%d %H:%M:%S'),
                    "backgroundColor": color,
                    "borderColor": color,
                }
            )
        context["eventos"] = json.dumps(eventos)
        return context


class CopiaTarefa(LoginRequiredMixin, TemplateView):
    template_name = "tarefas/tarefa_copy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarefa_id = kwargs.get('tarefa_id')
        context['tarefa_id'] = tarefa_id
        context['projetos'] = Projeto.objects.all()
        return context


@login_required
def copia_tarefa_post(request, tarefa_id):
    tarefa = Tarefa.objects.filter(pk=tarefa_id).get()
    projeto_id = request.POST.get('projeto_id')
    projeto = Projeto.objects.filter(pk=projeto_id).get()
    nova_tarefa = Tarefa()
    nova_tarefa.descricao = tarefa.descricao
    nova_tarefa.titulo = tarefa.titulo
    nova_tarefa.projeto = projeto
    nova_tarefa.status = Tarefa.StatusTarefa.ABERTA
    nova_tarefa.save()
    for checklist in tarefa.checklists.all():
        novo_checklist = TarefaChecklist()
        novo_checklist.tarefa = nova_tarefa
        novo_checklist.descricao = checklist.descricao
        novo_checklist.save()
    return redirect(reverse("tarefa-projeto-list", kwargs={"projeto_id": projeto_id}))