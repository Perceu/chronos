# produtividade/views.py

from logging import getLogger

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render

from chronos.tarefas.models import TarefaTempo
from chronos.tarefas.services import get_base_queryset

logger = getLogger(__name__)


@login_required
def dashboard(request):
    qs = get_base_queryset(request.empresa)

    total = qs.aggregate(total=Sum("duracao"))["total"]
    por_usuario = (
        qs.values("usuario__user__username")
        .annotate(total=Sum("duracao"))
        .order_by("-total")[:5]
    )

    diaria = (
        qs.annotate(dia=TruncDate("inicio"))
        .values("dia")
        .annotate(total=Sum("duracao"))
        .order_by("dia")[:30]
    )

    por_tarefa = (
        qs.values("tarefa__titulo")
        .annotate(total=Sum("duracao"))
        .order_by("-total")[:5]
    )

    abertos = TarefaTempo.objects.filter(tarefa__empresa=request.empresa, fim=None)

    alertas = []
    if abertos.count() > 0:
        alertas.append(f"{abertos.count()} tempos em aberto")
    logger.info(list(diaria))
    context = {
        "total_horas": total,
        "por_usuario": por_usuario,
        "diaria": list(diaria),
        "por_tarefa": por_tarefa,
        "tempos_abertos": abertos[:5],
        "alertas": alertas,
    }

    return render(request, "produtividade/dashboard.html", context)


@login_required
def produtividade_por_usuario(request):
    qs = get_base_queryset(request.empresa)
    dados = (
        qs.values("usuario__user__username")
        .annotate(total=Sum("duracao"))
        .order_by("-total")
    )
    return render(request, "produtividade/por_usuario.html", {"dados": dados})


@login_required
def produtividade_diaria(request):
    qs = get_base_queryset(request.empresa)
    dados = (
        qs.annotate(dia=TruncDate("inicio"))
        .values("dia")
        .annotate(total=Sum("duracao"))
        .order_by("dia")
    )

    return render(request, "produtividade/diaria.html", {"dados": dados})


@login_required
def ranking(request):
    qs = get_base_queryset(request.empresa)
    dados = (
        qs.values("usuario__user__username")
        .annotate(total=Sum("duracao"), registros=Sum(1))
        .order_by("-total")
    )
    return render(request, "produtividade/ranking.html", {"dados": dados})


@login_required
def tempo_por_tarefa(request):
    qs = get_base_queryset(request.empresa)
    dados = (
        qs.values("tarefa__titulo").annotate(total=Sum("duracao")).order_by("-total")
    )
    return render(request, "produtividade/por_tarefa.html", {"dados": dados})


@login_required
def tempos_abertos(request):
    dados = TarefaTempo.objects.filter(tarefa__empresa=request.empresa, fim=None)
    return render(request, "produtividade/tempos_abertos.html", {"dados": dados})
