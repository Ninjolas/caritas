from django.urls import path
from . import views

app_name = 'brecho'

urlpatterns = [
    path('', views.listagem, name='listagem'),
    path('novo/', views.criar_evento, name='criar_evento'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('<int:pk>/venda/', views.registrar_venda, name='registrar_venda'),
    path('<int:pk>/encerrar/', views.encerrar_evento, name='encerrar_evento'),
]
