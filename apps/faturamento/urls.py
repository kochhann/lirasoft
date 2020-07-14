from django.conf.urls import url
from django.urls import path, include

from . import views
from .views import *

urlpatterns = [
    path('nota_cobranca', NotaCobrancaList.as_view(), name='list_nota_cobranca'),
    path('nota_cobranca/editar/<int:pk>/', NotaCobrancaEdit.as_view(), name='edit_nota_cobranca'),
    path('nota_cobranca/criar/', NotaCobrancaCreate.as_view(), name='create_nota_cobranca'),
    path('nota_cobranca/deletar/<int:pk>/', NotaCobrancaDelete.as_view(), name='delete_nota_cobranca'),

]
