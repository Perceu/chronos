from django import forms
from chronos.projetos.models import Projeto


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ["nome", "cliente", "valor", "pago", "status"]
        widgets = {
            'valor': forms.TextInput(attrs={
                'class': "maskmoney",
            }),
        }
    
