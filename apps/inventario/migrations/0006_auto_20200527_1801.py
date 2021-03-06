# Generated by Django 3.0.3 on 2020-05-27 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0011_auto_20200518_1948'),
        ('inventario', '0005_auto_20200519_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='status',
            field=models.CharField(choices=[('1', 'DISPONIVEL'), ('2', 'LOCADO'), ('3', 'MANUTENCAO'), ('4', 'PERDIDO')], default='1', max_length=2, verbose_name='Status'),
        ),
        migrations.CreateModel(
            name='HistoricoEquipamento',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('descricao', models.CharField(blank=True, default='Padrão', max_length=100, null=True, verbose_name='Descrição')),
                ('status', models.CharField(default='1', max_length=2, verbose_name='Status')),
                ('data_evento', models.DateTimeField(blank=True, null=True)),
                ('empresa', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='empresa.Empresa')),
                ('equipamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Equipamento')),
            ],
        ),
    ]
