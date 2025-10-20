import django_filters
from chronos.projetos.models import Projeto


class ProjetoFilter(django_filters.FilterSet):
    class Meta:
        model = Projeto
        fields = ['status','pagamento', 'cliente']