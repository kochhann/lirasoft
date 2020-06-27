from django.urls import path, include
from .views import NotaCobrancaCreate

urlpatterns = [
    # path('nota_cobranca', NotaCobrancaList.as_view(), name='list_nota_cobranca'),
    # path('nota_cobranca/editar/<int:pk>/', NotaCobrancaEdit.as_view(), name='edit_nota_cobranca'),
    path('nota_cobranca/criar/', NotaCobrancaCreate.as_view(), name='create_nota_cobranca'),
    # path('nota_cobranca/deletar/<int:pk>/', NotaCobrancaoDelete.as_view(), name='delete_nota_cobranca'),
    # path('faturamento', FaturamentoList.as_view(), name='list_faturamentos'),
    # path('faturamento/editar/<int:pk>/', FaturamentoEdit.as_view(), name='edit_faturamentos'),
    # path('faturamento/criar/', FaturamentoCreate.as_view(), name='create_faturamentos'),
    # path('faturamento/deletar/<int:pk>/', FaturamentoDelete.as_view(), name='delete_faturamentos'),

]
