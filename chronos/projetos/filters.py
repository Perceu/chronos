from chronos.empresas.baseFilterSet import EmpresaFilterSet
from chronos.projetos.models import Projeto


class ProjetoFilter(EmpresaFilterSet):
    class Meta:
        model = Projeto
        fields = ['status','pagamento', 'cliente']