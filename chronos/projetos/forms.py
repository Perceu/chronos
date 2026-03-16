from django import forms
from chronos.empresas.baseForm import EmpresaModelForm
from chronos.projetos.models import Projeto


class ProjetoForm(EmpresaModelForm):
    class Meta:
        model = Projeto
        fields = ["nome", "cliente", "valor", "pagamento", "status"]
        widgets = {
            'valor': forms.TextInput(attrs={
                'class': "maskmoney",
            }),
        }
    
