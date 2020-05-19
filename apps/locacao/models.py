from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from apps.empresa.models import Empresa, Cliente
from apps.inventario.models import TipoEquipamento, Equipamento, Acessorio


class Contrato(models.Model):
    TIPO = (
        ('mensal', 'Mensal'),
        ('diaria', 'Diaria'),
    )
    codigo = models.AutoField("Código", primary_key=True, blank=False, null=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    cliente = models.OneToOneField(Cliente, on_delete=models.PROTECT)
    dataIni = models.DateField("Data Inicio")
    dataFim = models.DateField("Data Término", blank=True, null=True)
    valor = models.DecimalField("Preço", max_digits=100, decimal_places=2, blank=False,
                                default=0, null=False)
    tipo = models.CharField("Tipo", max_length=7, choices=TIPO, default='mensal')
    observacoes = models.CharField("Observações", max_length=300)
    obsnota = models.CharField("Observações", max_length=300, blank=True, null=True)
    valorproporcional = models.DecimalField("R$ Proporcional", max_digits=100, decimal_places=2,
                                            default=0, blank=True, null=True)
    emitir_nota = models.BooleanField("Emitir Nota", blank=True, default=True)
    emitir_boleto = models.BooleanField("Emitir Boleto", blank=True, default=True)
    emitir_contabil = models.BooleanField("Contabilizar", blank=True, default=True)
    data_cadastro = models.DateTimeField(blank=False, null=False)
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_contratos')

    def __str__(self):
        return self.codigo + ' - ' + self.cliente.razaoSocial


class QuadroAcessorio(models.Model):
    codigo = models.AutoField("Código", primary_key=True, blank=False, null=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
    acessorio = models.ForeignKey(Acessorio, on_delete=models.PROTECT)
    quantidade = models.IntegerField("Quantidade", blank=False, null=False, default=0)
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_quadro_acessorios')

    def __str__(self):
        return self.quantidade + ' - ' + self.acessorio.descricao


class QuadroEquipamentos(models.Model):
    codigo = models.AutoField("Código", primary_key=True, blank=False, null=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
    equipamento = models.ForeignKey(TipoEquipamento, on_delete=models.PROTECT)
    quantidade = models.IntegerField("Quantidade", blank=False, null=False, default=0)
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_quadro_equipamentos')

    def __str__(self):
        return self.quantidade + ' - ' + self.equipamento.marca + ' ' + self.equipamento.modelo


class ListaEquipamento(models.Model):
    codigo = models.AutoField("Código", primary_key=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_inclusao = models.DateTimeField(blank=False, null=False)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_lista_equipamentos')

    def __str__(self):
        return self.equipamento.serial
