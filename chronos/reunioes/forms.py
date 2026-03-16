from django import forms
from chronos.empresas.baseForm import EmpresaModelForm
from chronos.reunioes.models import Reuniao


class ReuniaoForm(EmpresaModelForm):
    class Meta:
        model = Reuniao
        fields = '__all__'
        exclude = ['empresa']

        widgets = {
            'inicio': forms.DateTimeInput(attrs={
                'class': "datetimepicker",
            }),
            'fim': forms.DateTimeInput(attrs={
                'class': "datetimepicker",
            }),
            'descricao': forms.Textarea(attrs={
                'class': "summernote",
            }),
        }