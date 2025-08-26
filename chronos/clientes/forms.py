from django import forms
from chronos.clientes.models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nome",
            "telefone",
            "observacoes",
        ]
        widgets = {
            'projeto': forms.HiddenInput(),
            'telefone': forms.TextInput(attrs={
                'data-inputmask': "'mask': '(99) [9]9999-9999'",
                'placeholder': '(99) 99999-9999',
                'type': 'tel',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': "summernote",
            }),
        }