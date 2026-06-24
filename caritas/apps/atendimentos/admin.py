from django.contrib import admin
from .models import Atendimento


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ['familia', 'tipo', 'data', 'paroquia', 'registrado_por']
    list_filter = ['tipo', 'paroquia', 'data']
    search_fields = ['familia__responsavel_nome']
    ordering = ['-data']
    readonly_fields = ['paroquia', 'registrado_por', 'criado_em']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(paroquia=request.user.paroquia)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'familia' and not request.user.is_superuser:
            from apps.familias.models import Familia
            kwargs['queryset'] = Familia.objects.filter(
                paroquia_responsavel=request.user.paroquia
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
