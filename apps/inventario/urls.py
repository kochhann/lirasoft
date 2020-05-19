from django.urls import path, include
from .views import *

urlpatterns = [
    path('tipo_equipamento', TipoEquipamentoList.as_view(), name='list_tipo_equip'),
    path('tipo_equipamento/editar/<int:pk>/', TipoEquipamentoEdit.as_view(), name='edit_tipo_equip'),
    path('tipo_equipamento/criar/', TipoEquipamentoCreate.as_view(), name='create_tipo_equip'),
    path('tipo_equipamento/deletar/<int:pk>/', TipoEquipamentoDelete.as_view(), name='delete_tipo_equip'),
    path('equipamento', EquipamentoList.as_view(), name='list_equipamentos'),
    path('equipamento/editar/<slug:pk>/', EquipamentoEdit.as_view(), name='edit_equipamentos'),
    path('equipamento/criar/', EquipamentoCreate.as_view(), name='create_equipamentos'),
    path('equipamento/deletar/<slug:pk>/', EquipamentoDelete.as_view(), name='delete_equipamentos'),
    path('acessorio', AcessorioList.as_view(), name='list_acessorios'),
    path('acessorio/editar/<int:pk>/', AcessorioEdit.as_view(), name='edit_acessorios'),
    path('acessorio/criar/', AcessorioCreate.as_view(), name='create_acessorios'),
    path('acessorio/deletar/<int:pk>/', AcessorioDelete.as_view(), name='delete_acessorios'),

]
