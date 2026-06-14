from django.urls import path
from . import views

app_name = 'bazar'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estoque/', views.estoque_listagem, name='estoque_listagem'),
    path('estoque/adicionar/', views.estoque_adicionar, name='estoque_adicionar'),
    path('doacoes/', views.doacoes_listagem, name='doacoes_listagem'),
    path('doacoes/registrar/', views.doacoes_registrar, name='doacoes_registrar'),
    path('vendas/', views.vendas_listagem, name='vendas_listagem'),
    path('vendas/registrar/', views.vendas_registrar, name='vendas_registrar'),
    path('empresas/', views.empresas_listagem, name='empresas_listagem'),
    path('empresas/nova/', views.empresas_form, name='empresa_nova'),
    path('empresas/<int:pk>/editar/', views.empresas_form, name='empresa_editar'),
    path('relatorio/', views.relatorio, name='relatorio'),
]
