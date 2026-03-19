import logging
from django import forms
from chronos.empresas.baseForm import EmpresaModelForm
from chronos.tarefas.models import Tarefa, TarefaChecklist, TarefaTempo
from django.forms.models import inlineformset_factory


class TarefaModelForm(EmpresaModelForm):
    class Meta:
        model = Tarefa
        fields = [
            "titulo",
            "descricao",
            "projeto",
            "data_entrega",
            "status",
            "usuario",
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
TarefaTempoForm = inlineformset_factory(Tarefa, TarefaTempo, fields=['inicio','fim', 'usuario'], extra=0)