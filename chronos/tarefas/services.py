from django.db.models import F, Sum, ExpressionWrapper, DurationField
from chronos.tarefas.models import TarefaTempo


def get_base_queryset(empresa):

    return TarefaTempo.objects.filter(
        tarefa__empresa=empresa
    ).exclude(
        fim=None
    ).annotate(
        duracao=ExpressionWrapper(
            F("fim") - F("inicio"),
            output_field=DurationField()
        )
    )