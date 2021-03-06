# Generated by Django 3.0.3 on 2020-07-08 02:05

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('locacao', '0006_auto_20200604_1233'),
        ('faturamento', '0002_remove_notacobranca_nomecliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notacobranca',
            name='contrato',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='cnpjcliente', chained_model_field='cliente', null=True, on_delete=django.db.models.deletion.CASCADE, to='locacao.Contrato'),
        ),
    ]
