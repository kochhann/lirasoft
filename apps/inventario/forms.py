from django.forms import ModelForm
from .models import Equipamento, TipoEquipamento

class EquipamentoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(EquipamentoForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoEquipamento.objects.filter(
            empresa=user.usuario.empresa, ativo=True
        )


    class Meta:
        model = Equipamento
        fields = ['tipo', 'status', 'serial']