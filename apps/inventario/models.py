from datetime import timezone
from django.db import models
from django.urls import reverse
from apps.empresa.models import Empresa


class TipoEquipamento(models.Model):
    codigo = models.AutoField("Código", primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, default='')
    marca = models.CharField("Marca", max_length=100, default='Padrão',  blank=True, null=True)
    modelo = models.CharField("Modelo", max_length=100, default='Padrão', blank=True, null=True)
    preco = models.DecimalField("Preço", max_digits=100, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('list_tipos_equipamento')

    def __str__(self):
        return self.marca + ' ' + self.modelo


class Equipamento(models.Model):
    STATUS = (
        ('1', 'DISPONIVEL'),
        ('2', 'LOCADO'),
        ('3', 'MANUTENCAO'),
        ('4', 'PERDIDO'),
    )
    serial = models.CharField("Serial", max_length=100,primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, default='')
    tipo = models.ForeignKey(TipoEquipamento, on_delete=models.PROTECT, default='')
    status = models.CharField("Status", max_length=2, choices=STATUS, default='1')
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_equipamentos')

    def __str__(self):
        return self.serial


class Acessorio(models.Model):
    codigo = models.AutoField("Código", primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, default='')
    descricao = models.CharField("Descrição", max_length=100, default='Padrão', blank=True, null=True)
    preco = models.DecimalField("Preço", max_digits=100, decimal_places=2, blank=True, null=True)
    quantidade = models.CharField("Quantidade", max_length=100, default='1', blank=True, null=True)
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_acessorios')

    def __str__(self):
        return self.descricao
