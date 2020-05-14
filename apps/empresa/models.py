from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    cnpjCpf = models.CharField("CNPJ / CPF", max_length=100, primary_key=True)
    nome = models.CharField("Nome", max_length=100)
    razaoSocial = models.CharField("Razão Social", max_length=100)
    responsavel = models.CharField("Rensponsável", max_length=100, blank=True, null=True)
    inscestadual = models.CharField("Inscricao Estadual", max_length=100, default='00000000')
    inscmunicipal = models.CharField("Inscricao Municipal", max_length=100, default='00000000')
    telefone = models.CharField("Telefone", max_length=100)
    endRua = models.CharField("Rua", max_length=100, default='01')
    endComplemento = models.CharField("Complemento", max_length=100, default='01')
    endCidade = models.CharField("Cidade", max_length=100, default='01')
    endUF = models.CharField("UF", max_length=100, default='RS')
    endCEP = models.CharField("CEP", max_length=10, default='00000000')
    email = models.CharField("E-mail", max_length=100)
    senhaWeb = models.CharField("Senha", max_length=100)
    site = models.CharField("Site", max_length=100, default='não cadastrado')
    nivel = models.CharField("Nivel", max_length=100, default='Matriz')

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    nome = models.CharField("Nome", max_length=100, blank=False, null=False)
    sobrenome = models.CharField("Sobrenome", max_length=100, blank=False, null=False)
    email = models.CharField("Email", max_length=100, blank=False, null=False)
    telefone = models.CharField("Telefone", max_length=100, blank=True, null=True)
    cargo = models.CharField("Cargo", max_length=100, blank=True, null=True)
    observacao = models.CharField("Observacao", max_length=200, blank=True, null=True)
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_usuarios')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Cliente(models.Model):
    TIPO = (
        ('01', 'Juridica'),
        ('02', 'Fisica'),
    )
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    cnpjCpf = models.CharField("CNPJ / CPF", max_length=100, primary_key=True, blank=False, null=False)
    nome = models.CharField("Nome", max_length=100)
    razaoSocial = models.CharField("Razão Social", max_length=100)
    responsavel = models.CharField("Rensponsável", max_length=100, blank=True, null=True)
    inscestadual = models.CharField("Inscricao Estadual", max_length=100, blank=True, null=True)
    inscmunicipal = models.CharField("Inscricao Municipal", max_length=100, blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=100, blank=True, null=True)
    email = models.CharField("E-mail", max_length=100, blank=True, null=True)
    site = models.CharField("Site", max_length=100, blank=True, null=True)
    endRua = models.CharField("Rua", max_length=100, blank=True, null=True)
    endComplemento = models.CharField("Complemento", max_length=100, blank=True, null=True)
    endCidade = models.CharField("Cidade", max_length=100, blank=True, null=True)
    endUF = models.CharField("UF", max_length=100, blank=True, null=True)
    endCEP = models.CharField("CEP", max_length=10, blank=True, null=True)
    senhaWeb = models.CharField("Senha", max_length=100, blank=True, null=True)
    tipo = models.CharField("Tipo", max_length=2, choices=TIPO, default='01')
    dataCriacao = models.DateTimeField(default=timezone.now)
    restricao = models.BooleanField("Restricao", blank=True, default=True)
    textorestricao = models.CharField("Observacao Restricao", max_length=200, default='', blank=True, null=True)
    ativo = models.BooleanField("Ativo", blank=True, default=True)
    data_desativado = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.ativo = False
        self.data_desativado = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('list_clientes')

    def __str__(self):
        return self.nome
