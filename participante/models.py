from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from lojista.models import Lojista
from django.urls import reverse
from django.core import validators
#from django.contrib.auth import get_user_model
from django_currentuser.db.models import CurrentUserField
from django.core.mail import EmailMessage



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, related_name='profile' )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    CHOICES_SEXO = (('M', 'Masculino'), ('F', 'Feminino'), ('P', 'Prefiro não dizer'))
    nome = models.CharField(max_length=100, blank=True)
    RG = models.CharField(max_length=40, blank=True, unique=False)
    CPF = models.CharField(max_length=14, blank=True, unique=True)
    #dataAtual = models.DateField(verbose_name=u'Data Atual', null=True, blank=True)  #mudar depois para nao colocar a data atual
    sexo = models.CharField(verbose_name=u'Sexo', max_length=1, choices=CHOICES_SEXO, blank=True, help_text=u'ex. M ou F ou P')
    foneFixo = models.CharField(verbose_name=u'Telefone Fixo', max_length=15, blank=True, help_text=u'ex. (85)3212-0000')
    foneCelular1 = models.CharField(verbose_name=u'Celular1', max_length=15, blank=True, help_text=u'ex. (85)98888-8675')
    foneCelular2 = models.CharField(verbose_name=u'Celular2', max_length=15, blank=True, help_text=u'ex. (85)98888-8675')
    foneCelular3 = models.CharField(verbose_name=u'Celular3', max_length=15, blank=True, help_text=u'ex. (85)98888-8675')
    whatsapp = models.CharField(max_length=15, blank=True, help_text=u'ex. (85)98888-8675')
    facebook = models.CharField(max_length=50, blank=True , help_text=u'ex. fb.com/nomenofacebook')
    twitter = models.CharField(max_length=50, blank=True)
    endereco = models.CharField(verbose_name=u'Endereço', max_length=150, blank=True)
    enderecoNumero = models.CharField(verbose_name=u'Nº Endereço', max_length=200, blank=True)
    enderecoComplemento = models.CharField(verbose_name=u'Complemento', max_length=100, blank=True)
    bairro = models.CharField(max_length=40, blank=True)
    cidade = models.CharField(max_length=50, blank=True, default=u'Teresina')
    estado = models.CharField(max_length=2, blank=True, default=u'PI')
    CEP = models.CharField(max_length=12, blank=True)
    observacao = models.TextField(verbose_name=u'Observação', max_length=1000, blank=True, null=True ) #, widget=forms.Textarea(attrs={'placeholder': 'Escreva aqui alguma observação caso seja necessário.'}))
    dataCadastro = models.DateTimeField(verbose_name=u'Cadastrado em', auto_now_add=True, editable=False)   #nao vai aparecer na tela
    cadastradoPor = CurrentUserField(verbose_name=u'Cadastrado Por', related_name='rel_cadastrado_por', editable=False)
    pergunta = models.TextField(verbose_name=u'Pergunta', max_length=50, blank=True, null=True ) #, widget=forms.Textarea(attrs={'placeholder': 'Escreva aqui alguma observação caso seja necessário.'}))
    ativo = models.BooleanField(default=True)
    pendente = models.BooleanField(default=True,verbose_name=u'Pendente' )
    termos_de_aceite = models.BooleanField(default=False,verbose_name=u'Termos de aceite para tratamento de dados pessoais' )

    def __str__(self):
        return 'Nome completo {}'.format(self.user.username)

    def get_absolute_url_edit(self):
        return reverse('participante:user_edit', args=[self.user.id])

    def get_absolute_url_detail(self):
        return reverse('participante:user_detail', args=[self.user.id])


class DocumentoFiscal(models.Model):
    #Lojista_Id = models.ForeignKey('Lojista', verbose_name=u'Loja', on_delete=models.SET_NULL, null=True)
    #Participante_Id = models.ForeignKey('Participante', default=1, verbose_name=u'Participante', on_delete=models.SET_NULL, null=True)
    user =  models.ForeignKey(User, related_name='rel_username', on_delete=models.PROTECT)
    lojista =  models.ForeignKey(Lojista, related_name='rel_lojista', null=False, blank=False, default=1, on_delete=models.PROTECT)
    vendedor = models.CharField(verbose_name=u'Nome do Vendedor', max_length=50, blank=True, null=True)
    numeroDocumento = models.CharField(verbose_name=u'Número do Documento', max_length=50, blank=False, null=False, unique=False)
    dataDocumento = models.DateField(verbose_name=u'Data do Documento', null=False, blank=False)
    valorDocumento = models.DecimalField(verbose_name=u'Valor do Documento', max_digits=15, decimal_places=2, blank=False, default=0, validators=[validators.MinValueValidator(100,message='O valor do documento deve ser maior que R$ 100,00 reais!')])
    compradoREDE = models.BooleanField(verbose_name=u'Comprou na maquininha da Rede?', default=False)
    compradoMASTERCARD = models.BooleanField(verbose_name=u'Comprou com Mastercard?', default=False)
    valorREDE = models.DecimalField(verbose_name=u'Valor na REDE', max_digits=7, decimal_places=2, editable=False, blank=True, default=0)   #depois posso nao mostrar
    photo = models.FileField(upload_to='docs/%Y/%m/%d', blank=True, verbose_name=u'Foto do documento fiscal')
    photo2 = models.FileField(upload_to='docs2/%Y/%m/%d', blank=True, verbose_name=u'Foto do comprovante do cartão')
    valorMASTERCARD = models.DecimalField(verbose_name=u'Valor no MASTERCARD', max_digits=7, decimal_places=2, editable=False, blank=True, default=0)   #depois posso nao mostrar
    valorVirtual = models.DecimalField(verbose_name=u'Valor com Bonificações', max_digits=20, decimal_places=2, editable=False, blank=True, default=0)   #depois posso nao mostrar
    dataCadastro = models.DateTimeField(verbose_name=u'Cadastrado em', auto_now_add=True, editable=False)
    cadastradoPor = CurrentUserField(verbose_name=u'Cadastrado Por', editable=False)
    status = models.BooleanField(verbose_name=u'Status', default=False)
    pendente = models.BooleanField(verbose_name=u'Pendente', default=True)
    observacao = models.TextField(verbose_name=u'Observação', max_length=1000, blank=True, null=True , default='Nenhuma')
    #impressaoHab = models.BooleanField(verbose_name=u'Status', default=False)
    qtdeCupom = models.IntegerField(blank=True, null=True, editable=False)

    def __str__(self):
        return 'Documento: {}'.format(self.numeroDocumento)

    class Meta:
        #ordering = ['Participante_Id', 'NumeroDocumento']
        verbose_name = (u'Documento Fiscal')
        verbose_name_plural = (u'Documentos Fiscais')

    def get_absolute_url(self):
        return reverse('participante:editdocfiscal', args=[self.id])

    def get_absolute_url_byop(self):
        return reverse('participante:editdocfiscalbyop', args=[self.id])

    # def get_cupons(self):
    #     cupons = 0
    #     if self.valorDocumento > 49.99:
    #         if self.compradoMASTERCARD and self.compradoREDE :
    #             self.valorVirtual = self.valorDocumento * 5
    #         elif self.compradoREDE:
    #             self.valorVirtual = self.valorDocumento * 3
    #         else:
    #             self.valorVirtual = self.valorDocumento

    #         cupons = self.valorVirtual // 50

    #     return cupons

    def get_cupons(self):
        cupons = 0
        if self.valorDocumento > 99.99:
            valor = self.valorDocumento // 100
            if self.compradoREDE:
                valor = valor * 3
            cupons = valor

        return cupons

    def send_email(self):
        body = "Estamos chegando no ultimo dia de campanha do Liquida Teresina 2023. \nPedimos que você cheque os seus documentos para verificar se está tudo certo, se não falta nenhuma foto dos seus cupons fiscal para que seus documentos sejam validados com sucesso e você possa concorrer para ganhar prêmios incriveis. \n \n Atenciosamente, \n \n Organização Liquida Teresina.\n www.liquidateresina.com.br"
        subject = "Liquida Teresina 2023 - Estamos chegando no último dia"
        email = EmailMessage(subject, body, to=[self.user.email])
        email.send()


class Transacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)
    quantidade_cupons = models.PositiveIntegerField(default=1)
    data_transacao = models.DateTimeField(auto_now_add=True)
    payload = models.TextField(blank=True, null=True)
    qrcode = models.ImageField(upload_to='qrcodes/%Y/%m/%d', blank=True, null=True, verbose_name='QR Code')
    processada = models.BooleanField(default=True)

    def __str__(self):
        return f'Transacao {self.id} - {self.user.username}'

# class Ticket(models.Model):
#     ticketUser =  models.ForeignKey(User, related_name='ticket_user_set', on_delete=models.PROTECT)
#     ticketDocumentoFiscal = models.ForeignKey(DocumentoFiscal, related_name='ticket_doc_set', null=False, blank=False, default=1, on_delete=models.PROTECT)
#     ticketOperador = CurrentUserField(verbose_name=u'Cadastrado Por', related_name='ticket_operador_set', editable=False)
#     ticketDataCriacao = models.DateTimeField(verbose_name=u'Cadastrado em', auto_now_add=True, editable=False)
#     ticketImpresso = models.BooleanField(default=False)
#     ticketDataImpressao = models.DateTimeField(null=True)
#     ticketLocal = models.CharField(max_length=15, null=False, blank=False, default=1,)
    
    # def __str__(self):
    #     return 'Cupom número: {}'.format(self.id)


    # def get_absolute_url(self):
    #     return reverse('cupom:details', args=[str(self.numeroCupom)])


    # def get_info(self):
    #     return 'Participante: {} CPF:{} Celular {} Documento Fiscal: {} Operador: {} Data de impressão: {} Data da compra: {} vendedor: {} '.format(
    #                                                                                                           self.user.profile.nome,
    #                                                                                                           self.user.profile.CPF,