import django_filters
from chronos.empresas.baseFilterSet import EmpresaFilterSet
from chronos.tarefas.models import Tarefa


class ProjetoTarefaFilter(EmpresaFilterSet):
    class Meta:
        model = Tarefa
        fields = ['projeto','user']