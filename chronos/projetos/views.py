from django.contrib.auth.mixins import LoginRequiredMixin
import logging
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
        self.logger = logging.getLogger(__name__)
        context = self.get_context_data()
        projeto = context["projeto"].pk
        url = self.request.GET.get("redirect", "projeto-list")
        if url == "tarefa-projeto-list":
            return reverse(url, kwargs={"projeto_id": projeto})
        return reverse(url)


class ProjetosDeleteView(LoginRequiredMixin, DeleteView):
    model = Projeto
    success_url = reverse_lazy("projeto-list")


class ProjetosDetailView(LoginRequiredMixin, DetailView):
    model = Projeto
