from django import forms

from chronos.empresas.baseForm import EmpresaModelForm
from chronos.projetos.models import Projeto


class ProjetoForm(EmpresaModelForm):
    class Meta:
        model = Projeto
        fields = [
            "nome",
            "cliente",
            "valor",
            "pagamento",
            "status",
            "senha_acesso",
            "pago",
            "progresso",
        ]
        widgets = {
            "valor": forms.TextInput(
                attrs={
                    "class": "maskmoney",
                }
            ),
        }

    # Campos públicos para o arquiteto enviar informações ao cliente
    mensagem_publica = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Digite uma mensagem pública para o cliente...",
            }
        ),
        label="Mensagem Pública",
    )

    link_publico = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "https://..."}
        ),
        label="Link Público",
    )

    arquivo_publico = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": ".pdf,.doc,.docx,.xls,.xlsx,.png,.jpg,.jpeg,.zip,.rar",
            }
        ),
        label="Arquivo Público",
    )
