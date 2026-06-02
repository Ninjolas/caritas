from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'perfil', 'paroquia', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Adicionais', {'fields': ('perfil', 'paroquia')}),
    )
