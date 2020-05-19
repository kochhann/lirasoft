# Generated by Django 3.0.3 on 2020-05-19 22:21

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0004_auto_20200519_1921'),
        ('empresa', '0011_auto_20200518_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('dataIni', models.DateField(verbose_name='Data Inicio')),
                ('dataFim', models.DateField(blank=True, null=True, verbose_name='Data Término')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Preço')),
                ('tipo', models.CharField(choices=[('mensal', 'Mensal'), ('diaria', 'Diaria')], default='mensal', max_length=7, verbose_name='Tipo')),
                ('observacoes', models.CharField(max_length=300, verbose_name='Observações')),
                ('obsnota', models.CharField(blank=True, max_length=300, null=True, verbose_name='Observações')),
                ('valorproporcional', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=100, null=True, verbose_name='R$ Proporcional')),
                ('emitir_nota', models.BooleanField(blank=True, default=True, verbose_name='Emitir Nota')),
                ('emitir_boleto', models.BooleanField(blank=True, default=True, verbose_name='Emitir Boleto')),
                ('emitir_contabil', models.BooleanField(blank=True, default=True, verbose_name='Contabilizar')),
                ('data_cadastro', models.DateTimeField(default=datetime.datetime(2020, 5, 19, 22, 21, 23, 917996, tzinfo=utc))),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('data_desativado', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='empresa.Cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='empresa.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='QuadroEquipamentos',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('quantidade', models.IntegerField(default=0, max_length=100, verbose_name='Quantidade')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('data_desativado', models.DateTimeField(blank=True, null=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locacao.Contrato')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='empresa.Empresa')),
                ('equipamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.TipoEquipamento')),
            ],
        ),
        migrations.CreateModel(
            name='QuadroAcessorio',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('quantidade', models.IntegerField(default=0, max_length=100, verbose_name='Quantidade')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('data_desativado', models.DateTimeField(blank=True, null=True)),
                ('acessorio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Acessorio')),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locacao.Contrato')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='empresa.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='ListaEquipamento',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('data_inclusao', models.DateTimeField(default=datetime.datetime(2020, 5, 19, 22, 21, 23, 922887, tzinfo=utc))),
                ('data_desativado', models.DateTimeField(blank=True, null=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locacao.Contrato')),
                ('equipamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Equipamento')),
            ],
        ),
    ]