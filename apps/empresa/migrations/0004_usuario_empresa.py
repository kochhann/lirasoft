# Generated by Django 3.0.3 on 2020-04-22 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0003_remove_usuario_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='empresa',
            field=models.ForeignKey(default=11771285000180, on_delete=django.db.models.deletion.PROTECT, to='empresa.Empresa'),
            preserve_default=False,
        ),
    ]
