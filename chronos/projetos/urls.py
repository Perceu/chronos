from django.urls import path
from chronos.projetos import views
from chronos.projetos import views_publicas

urlpatterns = [
    path('', views.ProjetosListView.as_view(), name="projeto-list"),
    path('criar', views.ProjetosCreateView.as_view(), name="projeto-add"),
    path('detalhe/<int:pk>', views.ProjetosDetailView.as_view(), name="projeto-detail"),
    path('editar/<int:pk>', views.ProjetosUpdateView.as_view(), name="projeto-update"),
    path('excluir/<int:pk>', views.ProjetosDeleteView.as_view(), name="projeto-delete"),
    path("projeto/publico/<uuid:token>/", views_publicas.projeto_publico, name="projeto-publico"),
    path("projeto/save/<uuid:token>/", views_publicas.save_informations, name="projeto-save")
]
