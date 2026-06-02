from django.urls import path

from . import views

app_name = 'familias'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('familias/cadastrar/', views.cadastrar_familia, name='cadastrar_familia'),
]
