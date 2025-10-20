from django.urls import path
from chronos.reunioes import views


urlpatterns = [
    path('nova', views.NovaReuniao.as_view(), name="nova-reuniao"),
    path('reunioes/<int:projeto_id>', views.ReunioesProjeto.as_view(), name="projetos-reuniao"),
    path('editar/<int:pk>', views.AlterarReuniao.as_view(), name="reuniao-editar"),
]
