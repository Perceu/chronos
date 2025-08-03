from django.urls import path
from chronos.tarefas import views


urlpatterns = [
    path('projeto/<int:projeto_id>', views.tarefas_projeto, name="tarefa-projeto-list"),
    path('play/<int:tarefa_id>', views.tarefas_start, name="tarefa-start"),
    path('pause/<int:tarefa_id>', views.tarefas_pause, name="tarefa-pause"),
    path('checklist/<int:checklist_id>', views.check_uncheck_checklist, name="checklist-check"),

    path('', views.TarefasListView.as_view(), name="tarefa-list"),
    path('criar', views.TarefasCreateView.as_view(), name="tarefa-add"),
    path('detalhe/<int:pk>', views.TarefasDetailView.as_view(), name="tarefa-detail"),
    path('editar/<int:pk>', views.TarefasUpdateView.as_view(), name="tarefa-update"),
    path('excluir/<int:pk>', views.TarefasDeleteView.as_view(), name="tarefa-delete"),
    path('kanban', views.KanbanTarefasView.as_view(), name="tarefa-kanban"),
    path('calendar', views.CalendarTarefasView.as_view(), name="tarefa-calendar"),
    path('copiar/<int:tarefa_id>', views.CopiaTarefa.as_view(), name="tarefa-copiar"),
    path('copiar/save/<int:tarefa_id>', views.copia_tarefa_post, name="tarefa-copiar-save"),
]
