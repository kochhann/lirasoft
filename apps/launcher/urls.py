from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('cadastrar_usuario', cadastrar_usuario, name="cadastrar_usuario"),
]
