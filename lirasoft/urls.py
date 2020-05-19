from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.launcher.urls')),
    path('empresa/', include('apps.empresa.urls')),
    path('faturamento/', include('apps.faturamento.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('locacao/', include('apps.locacao.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
