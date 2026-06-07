from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('', include('apps.accounts.urls')),
    path('', include('apps.familias.urls')),
    path('estoque/', include('apps.estoque.urls')),
    path('doacoes/', include('apps.doacoes.urls')),
]
