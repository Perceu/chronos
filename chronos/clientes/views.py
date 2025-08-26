from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from chronos.clientes.forms import ClienteForm
from chronos.clientes.models import Cliente


class ClientesListView(LoginRequiredMixin, ListView):
    model = Cliente
    paginate_by = 10


class ClientesCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("cliente-list")


class ClientesUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("cliente-list")


class ClientesDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy("cliente-list")


class ClientesDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
