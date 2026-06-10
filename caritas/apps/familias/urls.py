from django.urls import path

from . import views

app_name = 'familias'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('familias/', views.listar_familias, name='listar_familias'),
    path('familias/cadastrar/', views.cadastrar_familia, name='cadastrar_familia'),
    path('familias/<int:pk>/', views.detalhe_familia, name='detalhe_familia'),
    path('familias/<int:pk>/editar/', views.editar_familia, name='editar_familia'),
]
