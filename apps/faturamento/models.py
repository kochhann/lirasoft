from django.db import models
from django.utils import timezone

from apps.empresa.models import Empresa, Cliente
from apps.locacao.models import Contrato


class NotaCobranca(models.Model):
    numnota = models.IntegerField("Numero Nota", primary_key=True, blank=False, null=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, default='')
    datafechamento = models.DateField("Data Fechamento", blank=True, null=True)
    nomecliente = models.CharField("Nome Cliente", max_length=100, blank=True, null=True)
    cnpjcliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, blank=True, null=True)
    valor = models.DecimalField("Valor", max_digits=100, decimal_places=2, blank=True, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, blank=True, null=True)
    pedido = models.CharField("Pedido", max_length=100, default='N/A', blank=True, null=True)
    obsnota = models.CharField("Obs Nota", max_length=300, default='N/A', blank=True, null=True)
    cancelada = models.BooleanField("Cancelada", blank=True, default=False)
    data_inclusao = models.DateTimeField(blank=False, null=False)
    data_cancelada = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.cancelada = True
        self.data_cancelada = timezone.now()
        self.save()
