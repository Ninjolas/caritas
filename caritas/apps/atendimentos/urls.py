from django.urls import path
from . import views

app_name = 'atendimentos'

urlpatterns = [
    path('', views.listagem, name='listagem'),
    path('registrar/', views.registrar, name='registrar'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/remover/', views.remover, name='remover'),
]
