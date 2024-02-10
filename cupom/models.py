
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from participante.models import DocumentoFiscal
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField
from django.db import models
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile



# Create your models here.
class Cupom(models.Model):
    user =  models.ForeignKey(User, related_name='rel_cupom_participante', on_delete=models.PROTECT)
    documentoFiscal = models.ForeignKey(DocumentoFiscal, related_name='rel_cupom_doc', null=False, blank=False, default=1, on_delete=models.PROTECT)
    operador = CurrentUserField(verbose_name=u'Cadastrado Por', related_name='rel_cupom_operador', editable=False)
    dataCriacao = models.DateTimeField(verbose_name=u'Cadastrado em', auto_now_add=True, editable=False)
    impresso = models.BooleanField(default=False)
    dataImpressao = models.DateTimeField(null=True)
    
    def __str__(self):
        return 'Cupom número: {}'.format(self.id)


    def get_absolute_url(self):
        return reverse('cupom:details', args=[str(self.numeroCupom)])



    def get_info(self):
        return 'Participante: {} CPF:{} Celular {} Documento Fiscal: {} Operador: {} Data de impressão: {} Data da compra: {} vendedor: {} '.format(
                                                                                                              self.user.profile.nome,
                                                                                                              self.user.profile.CPF,
                                                                                                              self.user.profile.foneCelular1,
                                                                                                              self.documentoFiscal.numeroDocumento,
                                                                                                              self.operador.username,
                                                                                                              self.dataImpressao,
                                                                                                              self.documentoFiscal.dataDocumento,
                                                                                                              self.documentoFiscal.vendedor)
