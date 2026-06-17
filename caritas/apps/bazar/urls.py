from django.urls import path
from . import views

app_name = 'bazar'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Categorias
    path('categorias/', views.categorias_listagem, name='categorias_listagem'),
    path('categorias/nova/', views.categoria_form, name='categoria_nova'),
    path('categorias/<int:pk>/editar/', views.categoria_form, name='categoria_editar'),
    path('categorias/<int:pk>/remover/', views.categoria_remover, name='categoria_remover'),

    # Estoque
    path('estoque/', views.estoque_listagem, name='estoque_listagem'),
    path('estoque/adicionar/', views.estoque_adicionar, name='estoque_adicionar'),

    # Doações / Entradas
    path('doacoes/', views.doacoes_listagem, name='doacoes_listagem'),
    path('doacoes/registrar/', views.doacoes_registrar, name='doacoes_registrar'),

    # Vendas
    path('vendas/', views.vendas_listagem, name='vendas_listagem'),
    path('vendas/registrar/', views.vendas_registrar, name='vendas_registrar'),
    path('vendas/<int:pk>/comprovante/', views.comprovante, name='comprovante'),

    # Empresas
    path('empresas/', views.empresas_listagem, name='empresas_listagem'),
    path('empresas/nova/', views.empresas_form, name='empresa_nova'),
    path('empresas/<int:pk>/editar/', views.empresas_form, name='empresa_editar'),

    # Relatório
    path('relatorio/', views.relatorio, name='relatorio'),
]
