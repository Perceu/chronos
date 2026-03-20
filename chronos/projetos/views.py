from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from loguru import logger

from chronos.projetos.filters import ProjetoFilter
from chronos.projetos.forms import ProjetoForm
from chronos.projetos.models import (
    Projeto,
    ProjetoArquivo,
    ProjetoComentario,
    ProjetoLink,
)


class ProjetosListView(LoginRequiredMixin, ListView):
    model = Projeto
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProjetoFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


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
            form.fields["valor"].widget = forms.widgets.HiddenInput()
            form.fields["pago"].widget = forms.widgets.HiddenInput()
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        projeto = self.object
        self._salvar_campos_publicos(projeto, form)

        return response

    def _salvar_campos_publicos(self, projeto, form):
        """Salva os campos públicos (mensagem, link, arquivo) enviados pelo arquiteto"""

        # Salvar mensagem pública
        mensagem_publica = form.cleaned_data.get("mensagem_publica")
        if mensagem_publica:
            ProjetoComentario.objects.create(
                projeto=projeto,
                mensagem=mensagem_publica,
                autor_cliente=False,  # Enviado pelo arquiteto
            )

        # Salvar link público
        link_publico = form.cleaned_data.get("link_publico")
        if link_publico:
            ProjetoLink.objects.create(
                projeto=projeto,
                url=link_publico,
                enviado_por_cliente=False,  # Enviado pelo arquiteto
            )

        # Salvar arquivo público
        arquivo_publico = form.cleaned_data.get("arquivo_publico")
        if arquivo_publico:
            ProjetoArquivo.objects.create(
                projeto=projeto,
                arquivo=arquivo_publico,
                enviado_por_cliente=False,  # Enviado pelo arquiteto
            )


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
            form.fields["valor"].widget = forms.widgets.HiddenInput()
            form.fields["pago"].widget = forms.widgets.HiddenInput()
        return form

    def form_valid(self, form):
        response = super().form_valid(form)

        # Processar campos públicos (enviados pelo arquiteto, não pelo cliente)
        projeto = self.object
        self._salvar_campos_publicos(projeto, form)

        return response

    def _salvar_campos_publicos(self, projeto, form):
        """Salva os campos públicos (mensagem, link, arquivo) enviados pelo arquiteto"""

        # Salvar mensagem pública
        mensagem_publica = form.cleaned_data.get("mensagem_publica")
        if mensagem_publica:
            ProjetoComentario.objects.create(
                projeto=projeto,
                mensagem=mensagem_publica,
                autor_cliente=False,  # Enviado pelo arquiteto
            )

        # Salvar link público
        link_publico = form.cleaned_data.get("link_publico")
        if link_publico:
            ProjetoLink.objects.create(
                projeto=projeto,
                url=link_publico,
                enviado_por_cliente=False,  # Enviado pelo arquiteto
            )

        # Salvar arquivo público
        arquivo_publico = form.cleaned_data.get("arquivo_publico")
        if arquivo_publico:
            ProjetoArquivo.objects.create(
                projeto=projeto,
                arquivo=arquivo_publico,
                enviado_por_cliente=False,  # Enviado pelo arquiteto
            )


class ProjetosDeleteView(LoginRequiredMixin, DeleteView):
    model = Projeto
    success_url = reverse_lazy("projeto-list")


class ProjetosDetailView(LoginRequiredMixin, DetailView):
    model = Projeto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projeto = self.object

        # Carrega comentários do projeto
        context["comentarios"] = ProjetoComentario.objects.filter(
            projeto=projeto
        ).order_by("-criado_em")

        # Carrega arquivos do projeto
        context["arquivos"] = ProjetoArquivo.objects.filter(projeto=projeto)

        # Carrega links do projeto
        context["links"] = ProjetoLink.objects.filter(projeto=projeto).order_by(
            "-criado_em"
        )

        return context
