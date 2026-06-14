from django.urls import path
from . import views

app_name = 'cestas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('montar/', views.registrar_montagem, name='registrar_montagem'),
    path('doacao/', views.registrar_doacao_cesta, name='registrar_doacao_cesta'),
    path('entregar/', views.registrar_entrega, name='registrar_entrega'),
    path('entregas/', views.listagem_entregas, name='listagem_entregas'),
]
