from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Usuários (unificado)
    path('usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuarios/novo/', views.criar_usuario, name='criar_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/toggle/', views.toggle_usuario, name='toggle_usuario'),
    path('usuarios/<int:pk>/senha/', views.trocar_senha, name='trocar_senha'),

    # Paróquias
    path('paroquias/', views.gerenciar_paroquias, name='gerenciar_paroquias'),
    path('paroquias/nova/', views.criar_paroquia, name='criar_paroquia'),
    path('paroquias/<int:pk>/editar/', views.editar_paroquia, name='editar_paroquia'),
    path('paroquias/<int:pk>/remover/', views.remover_paroquia, name='remover_paroquia'),

    # Redirects para compatibilidade com URLs antigas
    path('coordenadores/', views.gerenciar_coordenadores, name='gerenciar_coordenadores'),
    path('voluntarios/', views.gerenciar_voluntarios, name='gerenciar_voluntarios'),
    path('voluntarios-bazar/', views.gerenciar_voluntarios_bazar, name='gerenciar_voluntarios_bazar'),
]
