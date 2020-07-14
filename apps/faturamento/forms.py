from django.forms import ModelForm
from django.shortcuts import render

from apps.empresa.models import Cliente
from apps.faturamento.models import NotaCobranca
from apps.locacao.models import Contrato


class NotaCobrancaForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(NotaCobrancaForm, self).__init__(*args, **kwargs)
        self.fields['cnpjcliente'].queryset = Cliente.objects.filter(
            empresa=user.usuario.empresa, ativo=True)
        self.fields['contrato'].queryset = Contrato.objects.all()


    class Meta:
        model = NotaCobranca
        fields = ['datafechamento', 'cnpjcliente', 'valor', 'contrato', 'pedido',
                  'obsnota']
