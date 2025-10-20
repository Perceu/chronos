from django import forms
from chronos.reunioes.models import Reuniao

class ReuniaoForm(forms.ModelForm):
    class Meta:
        model = Reuniao
        fields = '__all__'

        widgets = {
            'inicio': forms.DateTimeInput(attrs={
                'class': "datetimepicker",
            }),
            'fim': forms.DateTimeInput(attrs={
                'class': "datetimepicker",
            }),
        }