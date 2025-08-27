import logging
from django import forms
from chronos.tarefas.models import Tarefa, TarefaChecklist
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
                'data-inputmask': "'mask': '99/99/9999'",
                'placeholder':'dd/mm/yyyy',
                'type':'date',
            }),
            'descricao': forms.Textarea(attrs={
                'class': "summernote",
            }),
        }

TarefaChecklistForm = inlineformset_factory(Tarefa, TarefaChecklist, fields=['concluido', 'descricao'], extra=1)