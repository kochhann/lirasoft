# Generated by Django 3.0.3 on 2020-04-30 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0007_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='email',
            field=models.CharField(default='mail@mail.com', max_length=100, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='nome',
            field=models.CharField(default='nome', max_length=100, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='sobrenome',
            field=models.CharField(default='sobrenome', max_length=100, verbose_name='Sobrenome'),
            preserve_default=False,
        ),
    ]