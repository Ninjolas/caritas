from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('', views.listagem, name='listagem'),
    path('registrar/', views.registrar, name='registrar'),
    path('relatorio/', views.relatorio, name='relatorio'),
]
