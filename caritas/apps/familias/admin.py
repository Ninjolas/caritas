from django.contrib import admin

from .models import Dependente, Familia


class DependenteInline(admin.TabularInline):
    model = Dependente
    extra = 0


@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('responsavel_nome', 'id_interno', 'paroquia_responsavel', 'criado_em')
    search_fields = ('responsavel_nome', 'cpf', 'id_interno')
    inlines = [DependenteInline]


@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'familia', 'idade', 'genero')
