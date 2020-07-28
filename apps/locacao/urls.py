from django.urls import path, include
from .views import *

urlpatterns = [
    path('contrato', ContratoList.as_view(), name='list_contratos'),
    path('contrato/editar/<int:pk>/', ContratoEdit.as_view(), name='edit_contratos'),
    path('contrato/criar/', ContratoCreate.as_view(), name='create_contratos'),
    path('contrato/deletar/<int:pk>/', ContratoDelete.as_view(), name='delete_contratos'),
    path('quadro_equipamento/criar/<int:contrato_id>/', QuadroEquipamentoCreate.as_view(), name='create_quadro'),
    path('quadro_equipamento/editar/<int:pk>/', QuadroEquipamentoEdit.as_view(), name='edit_quadro'),
    path('quadro_equipamento/deletar/<int:pk>/', QuadroEquipamentoDelete.as_view(), name='delete_quadro'),
    path('quadro_acessorio/criar/<int:contrato_id>/', QuadroAcessorioCreate.as_view(), name='create_quadro_acessorio'),
    path('quadro_acessorio/editar/<int:pk>/', QuadroAcessorioEdit.as_view(), name='edit_quadro_acessorio'),
    path('quadro_acessorio/deletar/<int:pk>/', QuadroAcessorioDelete.as_view(), name='delete_quadro_acessorio'),
    path('lista_equipamento/criar/<int:contrato_id>/', ListaEquipamentoCreate.as_view(), name='create_lista'),
    path('vincular_equipamento/<int:gContrato>/', vincularEquipamento, name='vincular_equipamento'),
    path('grava_equipamento/<int:gContrato>/', gravaEquipamentoVinculado, name='grava_equipamento'),
    path('desvincular_equipamento/<int:gContrato>/', desvincularEquipamento, name='desvincular_equipamento'),
    path('grava_equipamento_desv/<int:gContrato>/', gravaEquipamentoDesvinculado, name='grava_equipamento_desv'),

]
