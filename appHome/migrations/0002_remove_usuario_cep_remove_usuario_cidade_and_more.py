# Generated by Django 5.2.1 on 2025-05-20 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appHome', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='cep',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='data_nascimento',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='email',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='logadouro',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='numero',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='senha',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='telefone',
        ),
    ]

