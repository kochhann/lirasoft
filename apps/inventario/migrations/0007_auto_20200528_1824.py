# Generated by Django 3.0.3 on 2020-05-28 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_auto_20200527_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoequipamento',
            name='empresa',
            field=models.CharField(blank=True, default='Padrão', max_length=100, null=True, verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='historicoequipamento',
            name='equipamento',
            field=models.CharField(blank=True, default='Padrão', max_length=100, null=True, verbose_name='Equipamento'),
        ),
    ]
