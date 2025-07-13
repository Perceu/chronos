from django.urls import path
from chronos.clientes import views


urlpatterns = [
    path('', views.ClientesListView.as_view(), name="cliente-list"),
    path('criar', views.ClientesCreateView.as_view(), name="cliente-add"),
    path('detalhe/<int:pk>', views.ClientesDetailView.as_view(), name="cliente-detail"),
    path('editar/<int:pk>', views.ClientesUpdateView.as_view(), name="cliente-update"),
    path('excluir/<int:pk>', views.ClientesDeleteView.as_view(), name="cliente-delete"),
]
