# Generated by Django 3.0.3 on 2020-05-28 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_auto_20200528_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoequipamento',
            name='status',
            field=models.CharField(blank=True, default='1', max_length=2, null=True, verbose_name='Status'),
        ),
    ]
