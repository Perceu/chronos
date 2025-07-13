from django.urls import path
from chronos.tarefas import views


urlpatterns = [
    path('projeto/<int:projeto_id>', views.tarefas_projeto, name="tarefa-projeto-list"),
    path('play/<int:tarefa_id>', views.tarefas_start, name="tarefa-start"),
    path('pause/<int:tarefa_id>', views.tarefas_pause, name="tarefa-pause"),

    path('', views.TarefasListView.as_view(), name="tarefa-list"),
    path('criar', views.TarefasCreateView.as_view(), name="tarefa-add"),
    path('detalhe/<int:pk>', views.TarefasDetailView.as_view(), name="tarefa-detail"),
    path('editar/<int:pk>', views.TarefasUpdateView.as_view(), name="tarefa-update"),
    path('excluir/<int:pk>', views.TarefasDeleteView.as_view(), name="tarefa-delete"),
    path('kanban', views.KanbanTarefasView.as_view(), name="tarefa-kanban"),
    path('calendar', views.CalendarTarefasView.as_view(), name="tarefa-calendar"),
]
