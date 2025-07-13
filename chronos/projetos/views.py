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


# Create your views here.
class ProjetosListView(ListView):
    model = Projeto


class ProjetosCreateView(CreateView):
    model = Projeto
    fields = ["nome", "cliente", "valor", "pago", "status"]


class ProjetosUpdateView(UpdateView):
    model = Projeto
    fields = ["nome", "cliente", "valor", "pago", "status"]

    def get_success_url(self):
        self.logger = logging.getLogger(__name__)
        context = self.get_context_data()
        projeto = context['projeto'].pk
        url = self.request.GET.get("redirect","projeto-list")
        if url == 'tarefa-projeto-list':
            return reverse(url, kwargs={"projeto_id": projeto}) 
        return reverse(url)
    


class ProjetosDeleteView(DeleteView):
    model = Projeto
    success_url = reverse_lazy("projeto-list")


class ProjetosDetailView(DetailView):
    model = Projeto
