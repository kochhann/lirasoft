from django.urls import path, include
from .views import *

urlpatterns = [
    path('usuarios', UsuariosList.as_view(), name='list_usuarios'),
    path('usuarios/editar/<int:pk>/', UsuariosEdit.as_view(), name='edit_usuarios'),
    path('usuarios/criar/', UsuariosCreate.as_view(), name='create_usuarios'),
    path('usuarios/deletar/<int:pk>/', UsuariosDelete.as_view(), name='delete_usuarios'),
    path('clientes/criar/', ClientesCreate.as_view(), name='create_clientes'),
    path('clientes', ClientesList.as_view(), name='list_clientes'),
    path('clientes/editar/<int:pk>/', ClientesEdit.as_view(), name='edit_clientes'),
    path('clientes/deletar/<int:pk>/', ClientesDelete.as_view(), name='delete_clientes'),

]
