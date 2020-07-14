# Generated by Django 3.0.3 on 2020-07-08 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0012_cidade_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='endCidade',
        ),
        migrations.RemoveField(
            model_name='empresa',
            name='endComplemento',
        ),
        migrations.AddField(
            model_name='empresa',
            name='cidade',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='empresa.Cidade'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='empresa.Estado'),
            preserve_default=False,
        ),
    ]