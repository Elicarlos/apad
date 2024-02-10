from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
from django.urls import reverse

class RamoAtividade(models.Model):
    """
    Model representando o ramo de atividade.
    """
    atividade = models.CharField(max_length=80, help_text='Informe o Ramo de Atividade. (exemplo: alimentação, vestuário, restaurante, etc.)')
    dataCadastro    = models.DateTimeField(verbose_name=u'Cadastrado em', auto_now_add=True, editable=False)   #nao vai aparecer na tela
    CadastradoPor   = CurrentUserField(verbose_name=u'Cadastrado Por', editable=False)
#    DataAlteracao   = models.DateTimeField(verbose_name=u'Alterado em', auto_now_add=True) #nao vai aparecer na tela
#    AlteradoPor_Id   = models.ForeignKey(User, blank=False, related_name='Cadastrado_por', editable=False, default=current_user.get_current_user)
    ativo = models.BooleanField(default=True)

    exclude =('ativo')

    class Meta:
        ordering = ['atividade']
        verbose_name = (u'ramo de Atividade')
        verbose_name_plural = (u'ramos de Atividades')

    def __str__(self):
        """
        String representando o Model object (in Admin site etc.)
        """
        return self.atividade


class Lojista(models.Model):
    CNPJLojista     = models.CharField(verbose_name=u'CNPJ do Lojista*', max_length=18, blank=False, null=True, unique=True, help_text=u'ex. 00.000.000/0000-00')
    IELojista       = models.CharField(verbose_name=u'Inscrição Estadual', max_length=14, blank=True, unique=False, null=True)
    razaoLojista    = models.CharField(verbose_name=u'Razão Social*', max_length=200, blank=True, null=True, help_text=u'Razão Social')
    fantasiaLojista = models.CharField(verbose_name=u'Nome Fantasia*', max_length=200, blank=False, help_text=u'Nome Fantasia')
    ramoAtividade   = models.ForeignKey('RamoAtividade', verbose_name=u'Ramo de Atividade*', on_delete=models.SET_NULL, null=True)
    dataCadastro    = models.DateTimeField(verbose_name=u'Cadastrado em', auto_now_add=True, editable=False)   #nao vai aparecer na tela
    CadastradoPor   = CurrentUserField(verbose_name=u'Cadastrado Por', editable=False)
    endereco        = models.CharField(verbose_name=u'Endereço', max_length=150, blank=True)
    telefone        = models.CharField(verbose_name=u'Telefone', max_length=150, blank=True, help_text=u'ex. (85)3212-0000')
#    CadastradoPor_Id = models.ForeignKey(User, editable=False, default=User.pk, on_delete=models.SET_NULL, null=True)
#    CadastradoPor_Id = models.ForeignKey(User, blank=False, related_name='Cadastrado_por', editable=False, default=current_user.get_current_user)
#    DataAlteracao   = models.DateTimeField(verbose_name=u'Alterado em', auto_now_add=True) #nao vai aparecer na tela
#    AlteradoPor_Id   = models.ForeignKey(User, blank=False, related_name='Cadastrado_por', editable=False, default=current_user.get_current_user)
    ativo           = models.BooleanField(default=True)

    exclude =('ativo')

    class Meta:
        ordering = ['fantasiaLojista']
        verbose_name = (u'lojista')
        verbose_name_plural = (u'lojistas')


    def __str__(self):
        """
        String representando o Objeto Participante.
        """
        return self.fantasiaLojista

    def get_absolute_url(self):
        return reverse('lojista:editlojista', args=[self.id])
