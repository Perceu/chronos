# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Projeto, ProjetoArquivo, ProjetoComentario, ProjetoLink


def projeto_publico(request, token):

    projeto = get_object_or_404(Projeto, token_publico=token)

    session_key = f"projeto_auth_{projeto.id}"

    # já autenticado
    if request.session.get(session_key):
        context = {
            "projeto": projeto,
            "comentarios": projeto.projetocomentario_set.all().order_by("-criado_em"),
            "arquivos": projeto.projetoarquivo_set.all(),
            "links": projeto.projetolink_set.all(),
        }
        return render(request, "cliente/projeto.html", context)

    erro = None

    if request.method == "POST":

        senha = request.POST.get("senha")

        if projeto.senha_expira_em and projeto.senha_expira_em < timezone.now():
            erro = "Senha expirada"

        elif senha == projeto.senha_acesso:
            request.session[session_key] = True
            return redirect(request.path)

        else:
            erro = "Senha inválida"

    return render(request, "cliente/login_projeto.html", {
        "projeto": projeto,
        "erro": erro
    })


def save_informations(request, token):

    projeto = get_object_or_404(Projeto, token_publico=token)

    session_key = f"projeto_auth_{projeto.id}"

    # já autenticado
    if request.session.get(session_key):
        if request.method == "POST":
            mensagem = request.POST.get("mensagem")
            arquivo = request.FILES.get("arquivo")
            link = request.POST.get("link_referencia")

            if mensagem:
                ProjetoComentario.objects.create(
                    projeto=projeto,
                    mensagem=mensagem,
                    autor_cliente=True
                )

            if arquivo:
                ProjetoArquivo.objects.create(
                    projeto=projeto,
                    arquivo=arquivo,
                    enviado_por_cliente=True
                )

            if link:
                ProjetoLink.objects.create(
                    projeto=projeto,
                    url=link,
                    enviado_por_cliente=True
                )

    return redirect("projeto-publico", token=token)