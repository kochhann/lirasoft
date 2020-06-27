from django.forms import ModelForm
from apps.empresa.models import Cliente
from apps.faturamento.models import NotaCobranca


class NotaCobrancaForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(NotaCobrancaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(
            empresa=user.usuario.empresa, ativo=True
        )

    class Meta:
        model = NotaCobranca
        fields = ['nomecliente', 'valor', 'contrato', 'pedido', 'obsnota']
