from django.contrib import admin

from chronos.tarefas.models import Tarefa,TarefaTempo, TarefaChecklist


class TarefaTempoInline(admin.TabularInline):
    model = TarefaTempo

class TarefaChecklistInline(admin.TabularInline):
    model = TarefaChecklist

class TarefaAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'titulo']
    list_filter = ['projeto']
    inlines = [TarefaTempoInline, TarefaChecklistInline]

admin.site.register(Tarefa, TarefaAdmin)
