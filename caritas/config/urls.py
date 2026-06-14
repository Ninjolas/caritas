from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('', include('apps.accounts.urls')),
    path('', include('apps.familias.urls')),
    path('estoque/', include('apps.estoque.urls')),
    path('doacoes/', include('apps.doacoes.urls')),
    path('atendimentos/', include('apps.atendimentos.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
    path('bazar/', include('apps.bazar.urls')),
    path('brecho/', include('apps.brecho.urls')),
    path('cestas/', include('apps.cestas.urls')),
    path('financeiro/', include('apps.financeiro.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
