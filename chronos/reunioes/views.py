from django.views.generic import CreateView, ListView, UpdateView
from chronos.reunioes.forms import ReuniaoForm
from chronos.reunioes.models import Reuniao
from django.urls import reverse_lazy


class NovaReuniao(CreateView):
    model = Reuniao
    form_class = ReuniaoForm
    template_name = 'reunioes/nova_reuniao_form.html'

    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy('projetos-reuniao', kwargs={'projeto_id': self.object.projeto.pk})


class AlterarReuniao(UpdateView):
    model = Reuniao
    form_class = ReuniaoForm
    template_name = 'reunioes/nova_reuniao_form.html'

    def get_success_url(self, **kwargs) -> str:
        scheme = self.get_object()
        return reverse_lazy('projetos-reuniao', kwargs={'projeto_id': scheme.projeto.pk})


class ReunioesProjeto(ListView):
    model = Reuniao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projeto = self.kwargs.get("projeto_id")
        if projeto:
            context["reunioes"] = Reuniao.objects.filter(projeto = projeto).all()
        return context