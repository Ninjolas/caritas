from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # admin: coordenadores
    path('coordenadores/', views.gerenciar_coordenadores, name='gerenciar_coordenadores'),
    path('coordenadores/novo/', views.criar_coordenador, name='criar_coordenador'),

    # admin: coordenadores do bazar
    path('coordenadores/novo-bazar/', views.criar_coordenador_bazar, name='criar_coordenador_bazar'),

    # coordenador: voluntários da paróquia
    path('voluntarios/', views.gerenciar_voluntarios, name='gerenciar_voluntarios'),
    path('voluntarios/novo/', views.criar_voluntario, name='criar_voluntario'),

    # coordenador do bazar: voluntários do bazar
    path('voluntarios-bazar/', views.gerenciar_voluntarios_bazar, name='gerenciar_voluntarios_bazar'),
    path('voluntarios-bazar/novo/', views.criar_voluntario_bazar, name='criar_voluntario_bazar'),

    # compartilhado
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/toggle/', views.toggle_usuario, name='toggle_usuario'),
    path('usuarios/<int:pk>/senha/', views.trocar_senha, name='trocar_senha'),
]
