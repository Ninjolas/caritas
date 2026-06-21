from django.urls import path
from . import views

app_name = 'bazar'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Catálogo
    path('catalogo/', views.catalogo_listagem, name='catalogo_listagem'),
    path('catalogo/novo/', views.catalogo_form, name='catalogo_novo'),
    path('catalogo/<int:pk>/editar/', views.catalogo_form, name='catalogo_editar'),
    path('catalogo/<int:pk>/remover/', views.catalogo_remover, name='catalogo_remover'),

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
    path('vendas/<int:pk>/comprovante/pdf/', views.comprovante_pdf, name='comprovante_pdf'),

    # Empresas
    path('empresas/', views.empresas_listagem, name='empresas_listagem'),
    path('empresas/nova/', views.empresas_form, name='empresa_nova'),
    path('empresas/<int:pk>/editar/', views.empresas_form, name='empresa_editar'),

    # Relatório
    path('relatorio/', views.relatorio, name='relatorio'),
]
