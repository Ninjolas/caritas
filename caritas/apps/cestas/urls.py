from django.urls import path
from . import views

app_name = 'cestas'

urlpatterns = [
    path('', views.listagem, name='listagem'),

    # Receber
    path('receber/', views.receber, name='receber'),
    path('recebidas/<int:pk>/editar/', views.editar_recebida, name='editar_recebida'),
    path('recebidas/<int:pk>/remover/', views.remover_recebida, name='remover_recebida'),

    # Montar/entregar
    path('montar/', views.montar, name='montar'),
    path('entregues/<int:pk>/editar/', views.editar_entregue, name='editar_entregue'),
    path('entregues/<int:pk>/remover/', views.remover_entregue, name='remover_entregue'),

    # Modelos
    path('modelos/', views.modelo_listagem, name='modelo_listagem'),
    path('modelos/novo/', views.modelo_form, name='modelo_novo'),
    path('modelos/<int:pk>/editar/', views.modelo_form, name='modelo_editar'),
    path('modelos/<int:pk>/remover/', views.modelo_remover, name='modelo_remover'),
]
