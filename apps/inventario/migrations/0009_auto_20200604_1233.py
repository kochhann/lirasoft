# Generated by Django 3.0.3 on 2020-06-04 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0008_auto_20200528_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoequipamento',
            name='status',
            field=models.CharField(default='1', max_length=2, verbose_name='Status'),
        ),
    ]