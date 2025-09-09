from django.contrib.auth.mixins import LoginRequiredMixin
from loguru import logger
from django import forms
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from chronos.projetos.models import Projeto
from chronos.projetos.forms import ProjetoForm


class ProjetosListView(LoginRequiredMixin, ListView):
    model = Projeto


class ProjetosCreateView(LoginRequiredMixin, CreateView):
    model = Projeto
    form_class = ProjetoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if "data" in kwargs.keys():
            querydict = kwargs["data"].copy()
            querydict["valor"] = float(
                querydict["valor"].replace(".", "").replace(",", ".")
            )
            kwargs["data"] = querydict
        return kwargs

    def get_form(self):
        form = super().get_form()
        if not self.request.user.has_perm("projetos.can_view_payment_info"):
            form.fields['valor'].widget = forms.widgets.HiddenInput()
            form.fields['pago'].widget = forms.widgets.HiddenInput()
        return form


class ProjetosUpdateView(LoginRequiredMixin, UpdateView):
    model = Projeto
    form_class = ProjetoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if "data" in kwargs.keys():
            querydict = kwargs["data"].copy()
            querydict["valor"] = float(
                querydict["valor"].replace(".", "").replace(",", ".")
            )
            kwargs["data"] = querydict
        if "instance" in kwargs.keys():
            kwargs["instance"].valor = str(kwargs["instance"].valor).replace(".", ",")
        return kwargs

    def get_success_url(self):
        context = self.get_context_data()
        projeto = context["projeto"].pk
        url = self.request.GET.get("redirect", "projeto-list")
        if url == "tarefa-projeto-list":
            return reverse(url, kwargs={"projeto_id": projeto})
        return reverse(url)

    def get_form(self):
        form = super().get_form()
        if not self.request.user.has_perm("projetos.can_view_payment_info"):
            form.fields['valor'].widget = forms.widgets.HiddenInput()
            form.fields['pago'].widget = forms.widgets.HiddenInput()
        return form


class ProjetosDeleteView(LoginRequiredMixin, DeleteView):
    model = Projeto
    success_url = reverse_lazy("projeto-list")


class ProjetosDetailView(LoginRequiredMixin, DetailView):
    model = Projeto
