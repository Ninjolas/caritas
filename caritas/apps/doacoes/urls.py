from django.urls import path
from . import views

app_name = 'doacoes'

urlpatterns = [
    path('', views.listagem, name='listagem'),
    path('registrar/', views.registrar, name='registrar'),
]
