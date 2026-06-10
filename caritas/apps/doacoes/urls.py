from django.urls import path
from . import views

app_name = 'doacoes'

urlpatterns = [
    path('', views.listagem, name='listagem'),
    path('registrar/', views.registrar, name='registrar'),
    path('<int:pk>/editar/', views.editar_doacao, name='editar_doacao'),
    path('<int:pk>/remover/', views.remover_doacao, name='remover_doacao'),
]
