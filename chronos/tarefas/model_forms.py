import logging
from django import forms
from chronos.tarefas.models import Tarefa, TarefaChecklist, TarefaTempo
from django.forms.models import inlineformset_factory


class TarefaModelForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = [
            "titulo",
            "descricao",
            "projeto",
            "data_entrega",
            "status",
        ]
        widgets = {
            'data_entrega': forms.DateInput(attrs={
                'class': 'datepicker',
            }),
            'descricao': forms.Textarea(attrs={
                'class': "summernote",
            }),
        }


TarefaChecklistForm = inlineformset_factory(Tarefa, TarefaChecklist, fields=['concluido', 'descricao'], extra=1)


TarefaTempoForm = inlineformset_factory(Tarefa, TarefaTempo, fields=['inicio','fim'], extra=0)
