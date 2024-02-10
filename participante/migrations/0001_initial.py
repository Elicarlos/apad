# Generated by Django 3.2.20 on 2023-08-25 13:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lojista', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='users/%Y/%m/%d')),
                ('nome', models.CharField(blank=True, max_length=100)),
                ('RG', models.CharField(blank=True, max_length=40, unique=True)),
                ('CPF', models.CharField(blank=True, max_length=14, unique=True)),
                ('sexo', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('P', 'Prefiro não dizer')], help_text='ex. M ou F ou P', max_length=1, verbose_name='Sexo')),
                ('foneFixo', models.CharField(blank=True, help_text='ex. (85)3212-0000', max_length=15, verbose_name='Telefone Fixo')),
                ('foneCelular1', models.CharField(blank=True, help_text='ex. (85)98888-8675', max_length=15, verbose_name='Celular1')),
                ('foneCelular2', models.CharField(blank=True, help_text='ex. (85)98888-8675', max_length=15, verbose_name='Celular2')),
                ('foneCelular3', models.CharField(blank=True, help_text='ex. (85)98888-8675', max_length=15, verbose_name='Celular3')),
                ('whatsapp', models.CharField(blank=True, help_text='ex. (85)98888-8675', max_length=15)),
                ('facebook', models.CharField(blank=True, help_text='ex. fb.com/nomenofacebook', max_length=50)),
                ('twitter', models.CharField(blank=True, max_length=50)),
                ('endereco', models.CharField(blank=True, max_length=150, verbose_name='Endereço')),
                ('enderecoNumero', models.CharField(blank=True, max_length=200, verbose_name='Nº Endereço')),
                ('enderecoComplemento', models.CharField(blank=True, max_length=100, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=40)),
                ('cidade', models.CharField(blank=True, default='Teresina', max_length=50)),
                ('estado', models.CharField(blank=True, default='PI', max_length=2)),
                ('CEP', models.CharField(blank=True, max_length=12)),
                ('observacao', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Observação')),
                ('dataCadastro', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
                ('pergunta', models.TextField(blank=True, max_length=50, null=True, verbose_name='Pergunta')),
                ('ativo', models.BooleanField(default=True)),
                ('pendente', models.BooleanField(default=True, verbose_name='Pendente')),
                ('termos_de_aceite', models.BooleanField(default=False, verbose_name='Termos de aceite para tratamento de dados pessoais')),
                ('cadastradoPor', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_cadastrado_por', to=settings.AUTH_USER_MODEL, verbose_name='Cadastrado Por')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoFiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendedor', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome do Vendedor')),
                ('numeroDocumento', models.CharField(max_length=50, verbose_name='Número do Documento')),
                ('dataDocumento', models.DateField(verbose_name='Data do Documento')),
                ('valorDocumento', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(100, message='O valor do documento deve ser maior que R$ 100,00 reais!')], verbose_name='Valor do Documento')),
                ('compradoREDE', models.BooleanField(default=False, verbose_name='Comprou na maquininha da Rede?')),
                ('compradoMASTERCARD', models.BooleanField(default=False, verbose_name='Comprou com Mastercard?')),
                ('valorREDE', models.DecimalField(blank=True, decimal_places=2, default=0, editable=False, max_digits=7, verbose_name='Valor na REDE')),
                ('photo', models.FileField(blank=True, upload_to='docs/%Y/%m/%d', verbose_name='Foto do documento fiscal')),
                ('photo2', models.FileField(blank=True, upload_to='docs2/%Y/%m/%d', verbose_name='Foto do comprovante do cartão')),
                ('valorMASTERCARD', models.DecimalField(blank=True, decimal_places=2, default=0, editable=False, max_digits=7, verbose_name='Valor no MASTERCARD')),
                ('valorVirtual', models.DecimalField(blank=True, decimal_places=2, default=0, editable=False, max_digits=20, verbose_name='Valor com Bonificações')),
                ('dataCadastro', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('pendente', models.BooleanField(default=True, verbose_name='Pendente')),
                ('observacao', models.TextField(blank=True, default='Nenhuma', max_length=1000, null=True, verbose_name='Observação')),
                ('qtdeCupom', models.IntegerField(blank=True, editable=False, null=True)),
                ('cadastradoPor', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cadastrado Por')),
                ('lojista', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='rel_lojista', to='lojista.lojista')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rel_username', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Documento Fiscal',
                'verbose_name_plural': 'Documentos Fiscais',
            },
        ),
    ]
