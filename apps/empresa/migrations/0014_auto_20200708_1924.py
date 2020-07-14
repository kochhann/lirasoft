# Generated by Django 3.0.3 on 2020-07-08 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0013_auto_20200708_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='endCidade',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='endUF',
        ),
        migrations.AddField(
            model_name='cliente',
            name='cidade',
            field=models.ForeignKey(default=4266, on_delete=django.db.models.deletion.PROTECT, to='empresa.Cidade'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.PROTECT, to='empresa.Estado'),
            preserve_default=False,
        ),
    ]
