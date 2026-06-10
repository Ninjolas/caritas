from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.listagem, name='listagem'),
    path('entrada/', views.entrada, name='entrada'),
    path('<int:pk>/editar/', views.editar_item, name='editar_item'),
    path('<int:pk>/remover/', views.remover_item, name='remover_item'),
]
