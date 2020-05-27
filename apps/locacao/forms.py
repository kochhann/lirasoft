from django.forms import ModelForm, forms, TextInput
from .models import QuadroEquipamentos, Contrato, QuadroAcessorio, ListaEquipamento
from apps.inventario.models import TipoEquipamento, Acessorio, Equipamento
from ..empresa.models import Cliente


class VincularEquipamento(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(QuadroEquipamentoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ListaEquipamento
        fields = ['equipamento']
        widgets = {'equipamento': TextInput()}


class QuadroEquipamentoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(QuadroEquipamentoForm, self).__init__(*args, **kwargs)
        self.fields['equipamento'].queryset = TipoEquipamento.objects.filter(
            empresa=user.usuario.empresa, ativo=True
        )

    class Meta:
        model = QuadroEquipamentos
        fields = ['equipamento', 'quantidade']


class QuadroAcessorioForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(QuadroAcessorioForm, self).__init__(*args, **kwargs)
        self.fields['acessorio'].queryset = Acessorio.objects.filter(
            empresa=user.usuario.empresa, ativo=True
        )

    class Meta:
        model = QuadroAcessorio
        fields = ['acessorio', 'quantidade']


class ListaEquipamentoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ListaEquipamentoForm, self).__init__(*args, **kwargs)
        # self.fields['equipamento'].queryset = Equipamento.objects.filter(
        #     empresa=user.usuario.empresa, ativo=True
        # )

    class Meta:
        model = ListaEquipamento
        fields = ['equipamento']
        widgets = {'equipamento': TextInput()}


class ContratoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(
            empresa=user.usuario.empresa, ativo=True
        )

    class Meta:
        model = Contrato
        fields = ['tipo', 'cliente', 'dataIni', 'dataFim', 'valor', 'emitir_nota',
                  'emitir_boleto', 'emitir_contabil', 'observacoes', 'obsnota']