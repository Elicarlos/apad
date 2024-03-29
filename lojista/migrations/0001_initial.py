# Generated by Django 3.2.20 on 2023-08-25 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RamoAtividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atividade', models.CharField(help_text='Informe o Ramo de Atividade. (exemplo: alimentação, vestuário, restaurante, etc.)', max_length=80)),
                ('dataCadastro', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
                ('ativo', models.BooleanField(default=True)),
                ('CadastradoPor', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cadastrado Por')),
            ],
            options={
                'verbose_name': 'ramo de Atividade',
                'verbose_name_plural': 'ramos de Atividades',
                'ordering': ['atividade'],
            },
        ),
        migrations.CreateModel(
            name='Lojista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CNPJLojista', models.CharField(help_text='ex. 00.000.000/0000-00', max_length=18, null=True, unique=True, verbose_name='CNPJ do Lojista*')),
                ('IELojista', models.CharField(blank=True, max_length=14, null=True, verbose_name='Inscrição Estadual')),
                ('razaoLojista', models.CharField(blank=True, help_text='Razão Social', max_length=200, null=True, verbose_name='Razão Social*')),
                ('fantasiaLojista', models.CharField(help_text='Nome Fantasia', max_length=200, verbose_name='Nome Fantasia*')),
                ('dataCadastro', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
                ('endereco', models.CharField(blank=True, max_length=150, verbose_name='Endereço')),
                ('telefone', models.CharField(blank=True, help_text='ex. (85)3212-0000', max_length=150, verbose_name='Telefone')),
                ('ativo', models.BooleanField(default=True)),
                ('CadastradoPor', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cadastrado Por')),
                ('ramoAtividade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lojista.ramoatividade', verbose_name='Ramo de Atividade*')),
            ],
            options={
                'verbose_name': 'lojista',
                'verbose_name_plural': 'lojistas',
                'ordering': ['fantasiaLojista'],
            },
        ),
    ]
