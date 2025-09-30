import django_filters
from chronos.tarefas.models import Tarefa


class ProjetoTarefaFilter(django_filters.FilterSet):
    class Meta:
        model = Tarefa
        fields = ['projeto',]