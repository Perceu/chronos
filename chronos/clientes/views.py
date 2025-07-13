from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from chronos.clientes.models import Cliente

# Create your views here.
class ClientesListView(ListView):
    model = Cliente
    paginate_by = 10

class ClientesCreateView(CreateView):
    model = Cliente
    fields = ["nome", "telefone", "observacoes"]

class ClientesUpdateView(UpdateView):
    model = Cliente
    fields = ["nome", "telefone", "observacoes"]

class ClientesDeleteView(DeleteView):
    model = Cliente
    success_url = reverse_lazy("cliente-list")

class ClientesDetailView(DetailView):
    model = Cliente