from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import DocumentoFiscal
from lojista.models import Lojista
from localflavor.br.forms import *
from localflavor.br.br_states import STATE_CHOICES
from localflavor.br.forms import BRCPFField, BRZipCodeField
from django.core.exceptions import ValidationError
from datetime import datetime

from datetime import date, datetime




class UserAddFiscalDocFormSuperuserNovo(forms.ModelForm):
    # Esconde o campo 'numeroDocumento' no template
    numeroDocumento = forms.CharField(widget=forms.HiddenInput(), required=False)
    # Define a data atual como valor inicial para o campo data
    dataDocumento = forms.DateField(widget=forms.HiddenInput(), initial=datetime.today)
    
    class Meta:
        model = DocumentoFiscal
        fields = ['valorDocumento', 'dataDocumento', 'numeroDocumento']
        widgets = {
            'valorDocumento': forms.TextInput(attrs={'placeholder': 'Valor'}),
            'dataDocumento': forms.HiddenInput(),  # Será a data atual, não precisa ser editado
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Digite seu usuario', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Digite sua senha', 'class':'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':'Senha* (mínimo de 8 caracteres)'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':'Confirmação de senha*'}))
    username = BRCPFField(required=True, max_length=14, min_length=11, widget=forms.TextInput(attrs={'placeholder':'CPF*', 'autocomplete':'off',
                                                                                                'class':'cpf', 'cpf':'id_CPF'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'Email*', 'autocomplete':'off'}))
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise ValidationError("CPF do participante já está cadastrado!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Esse email já está vinculado a outro perfil.')
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas digitadas não correspondem.')
        return cd['password2']

class ProfileRegistrationForm(forms.ModelForm):
    CHOICES_SEXO = (('M', 'Masculino'), ('F', 'Feminino'), ('P', 'Prefiro não dizer'))
    CHOICES_STATES = (('PI', 'Piauí'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
              ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
              ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
              ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
              ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
              ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'),
              ('TO', 'Tocantins'))
    #sexo = forms.ChoiceField(choices=CHOICES_SEXO, widget=forms.Select(attrs={'id' : 'sexo'}))
    #estado = forms.ChoiceField(required=True, choices=STATE_CHOICES, widget=forms.Select(attrs={'id' : 'estados'}))
    #pergunta = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Sua resposta', 'autocomplete':'off'}))
    nome = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Nome Completo*', 'autocomplete':'off'}))
    #RG = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'RG*', 'autocomplete':'off'}))
    CPF = BRCPFField(required=False, max_length=14, min_length=11, widget=forms.TextInput(attrs={'placeholder':'CPF*',
                                                                                                'class':'cpf', 'type':'hidden'}))
    foneCelular1 = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Celular*',
                                                                                  'class': 'phone_with_ddd', 'autocomplete':'off'}))
    #whatsapp = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Whatsapp', 'class': 'phone_with_ddd', 'autocomplete':'off'}))
    #facebook = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Facebook', 'autocomplete':'off'}))
    #twitter = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Twitter', 'autocomplete':'off'}) )
    #endereco = forms.CharField( required=True, widget=forms.TextInput(attrs={'placeholder':'Endereço*', 'autocomplete':'off'}))
    #enderecoNumero = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Nº da casa', 'autocomplete':'off'}))
    #enderecoComplemento = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Complemento', 'autocomplete':'off'}))
    #bairro = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Bairro*', 'autocomplete':'off'}))
    #cidade = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Cidade*', 'autocomplete':'off'}))
    #estado = forms.ChoiceField(required=True, choices=CHOICES_STATES, widget=forms.Select(attrs={'id' : 'estados'}))
    # estado = forms.ChoiceField(required=True, widget=forms.TextInput(attrs={'placeholder':'Estado*', 'autocomplete':'off'}))
    #CEP = BRZipCodeField(required=False, label='Cep*' , widget=forms.TextInput(attrs={'class':'cep', 'placeholder':'CEP*', 'autocomplete':'off'}))
    #pergunta = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Promoção'}))

    class Meta:
        model = Profile
        fields = ('nome', 'CPF', 'sexo', 'foneFixo', 'foneCelular1', 'CEP', 'foneCelular2', 'foneCelular3',
                  'whatsapp','facebook','twitter','endereco','enderecoNumero','enderecoComplemento' ,'bairro','cidade', 'estado',
                   'pergunta' )
        exclude = ('user', 'RG', 'sexo', 'CEP','dataCadastro','endereco','enderecoNumero','enderecoComplemento' ,'bairro','cidade', 'estado', 'cadastradoPor', 'ativo', 'pendente')

    def clean_RG(self):
        RG = self.cleaned_data.get('RG')
        RG_qs = Profile.objects.filter(RG=RG)
        if RG_qs.exists():
            raise ValidationError("O participante com esse RG já está cadastrado!")
        return RG




class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.Select(attrs={'type' : 'hidden'}))
    last_name = forms.CharField(required=False, widget=forms.Select(attrs={'type' : 'hidden'}))
    user_permissions = forms.ChoiceField(required=False,widget=forms.Select(attrs={'type' : 'hidden'}))
    groups = forms.ChoiceField(required=False,widget=forms.Select(attrs={'type' : 'hidden'}))
    is_superuser = forms.BooleanField(required=False,widget=forms.Select(attrs={'type' : 'hidden'}))
    is_staff = forms.BooleanField(required=False,widget=forms.Select(attrs={'type' : 'hidden'}))
    password = forms.CharField(required=False)
    date_joined = forms.DateField(required=False,widget=forms.Select(attrs={'type' : 'hidden'}))
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'ativo': forms.HiddenInput,
            'user_permissions': forms.HiddenInput,
            'groups': forms.HiddenInput,
            'is_superuser': forms.HiddenInput,
            'last_login': forms.HiddenInput,
            'is_staff': forms.HiddenInput,
            'password': forms.HiddenInput,
            'is_active': forms.HiddenInput,
            'date_joined': forms.HiddenInput,
        }
        exclude = ('password','username',)
        
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        # Se você deseja garantir que `is_active` nunca seja alterado, não o inclua no formulário
        if 'is_active' in self.fields:
            del self.fields['is_active']


class UserAddCoupom(forms.ModelForm):
    numeroDoCupom = forms.CharField(label='Numero do cupom')
    valorDoCupom = forms.DecimalField(label='Valor do cupom')


class UserAddFiscalDocForm(forms.ModelForm):
    lojista_cnpj = BRCNPJField(label='CNPJ', initial='11.630.639/0001-77',  required=True, max_length=18, widget=forms.HiddenInput(attrs={'class':'cnpj', 'autocomplete':'off'}))
    dataDocumento = forms.DateField(label='Data do pagamento',widget=forms.TextInput(attrs={ 'class':'date', 'autocomplete':'off'}))
    valorDocumento = forms.DecimalField(max_digits=8, decimal_places=2, localize=True, label='Valor', widget=forms.TextInput(attrs={'autocomplete':'off', 'id': 'id_add_doc'}))
    
    numeroDocumento = forms.CharField(label='Nº Comprovante', widget=forms.TextInput(attrs={ 'autocomplete':'off'}))
    photo = forms.FileField(label='Comprovante PIX', required=True)
  
    class Meta:
        model = DocumentoFiscal
        fields = ('lojista_cnpj', 'numeroDocumento', 'dataDocumento', 'valorDocumento', 'photo')
        exclude = ('photo2',)
        widgets = {
            #'lojista': forms.HiddenInput,
            'user': forms.HiddenInput,
            'pendente': forms.HiddenInput,
            'observacao': forms.HiddenInput,
            'valorREDE': forms.HiddenInput,
            'valorMASTERCARD': forms.HiddenInput,
            'valorVirtual': forms.HiddenInput,
        }
        
        

    def clean_numeroDocumento(self):
        numeroDocumento = self.cleaned_data.get('numeroDocumento')
        lojista_cnpj = self.cleaned_data.get('lojista_cnpj')
        lojista = Lojista.objects.get(CNPJLojista=lojista_cnpj)
        if numeroDocumento and DocumentoFiscal.objects.filter(lojista=lojista, numeroDocumento=numeroDocumento).exists():
            raise forms.ValidationError(u'Um documento com este número já foi lançado')
        return numeroDocumento

class UserAddFiscalDocFormSuperuser(UserAddFiscalDocForm):
    photo = forms.FileField(label='Documento fiscal', required=False)
    photo2 = forms.FileField(label='Comprovante do cartão', required=False)


class DocumentoFiscalEditFormOp(forms.ModelForm):
    class Meta:
        model = DocumentoFiscal
        exclude = ('vendedor','photo','photo2', 'user', 'lojista' ,'compradoREDE','qtdeCupom','compradoMASTERCARD')
        fields = '__all__'

class DocumentoFiscalEditForm(forms.ModelForm):
    class Meta:
        model = DocumentoFiscal
        exclude = ('vendedor','compradoREDE', 'compradoMASTERCARD', 'photo2','pendente','user', 'lojista')
        fields = '__all__'

class DocumentoFiscalValidaForm(forms.ModelForm):
    class Meta:
        model = DocumentoFiscal
        exclude = ('lojista','user','vendedor','compradoREDE','qtdeCupom','compradoMASTERCARD' )
        fields = '__all__'
        widgets = {
            'status': forms.HiddenInput,

        }


class ProfileEditForm(forms.ModelForm):
    CHOICES_SEXO = (('M', 'Masculino'), ('F', 'Feminino'), ('P', 'Prefiro não dizer'))
    sexo = forms.ChoiceField(choices=CHOICES_SEXO, widget=forms.Select(attrs={'id' : 'sexo'}))
    estado = forms.ChoiceField(required=True, choices=STATE_CHOICES, widget=forms.Select(attrs={'id' : 'estados'}))
    pergunta = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Sua resposta'}))
    nome = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Nome Completo*'}))
    RG = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'RG*'}))
    CPF = BRCPFField(required=True, max_length=14, min_length=11, widget=forms.TextInput(attrs={'placeholder':'CPF*',
                                                                                                'class':'cpf'}))
    foneCelular1 = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Celular*',
                                                                                  'class': 'phone_with_ddd'}))
    whatsapp = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Whatsapp',
                                                                                  'class': 'phone_with_ddd'}))
    facebook = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Facebook'}))
    twitter = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Twitter'}) )
    endereco = forms.CharField( required=True, widget=forms.TextInput(attrs={'placeholder':'Endereço*'}))
    enderecoNumero = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Nº da casa'}))
    enderecoComplemento = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Complemento'}))
    bairro = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Bairro*'}))
    cidade = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Cidade*'}))
    estado = forms.ChoiceField(required=True, choices=STATE_CHOICES, widget=forms.Select(attrs={'id' : 'estados'}))
    CEP = BRZipCodeField(required=False, label='Cep*' , widget=forms.TextInput(attrs={'class':'cep', 'placeholder':'CEP*'}))
    pergunta = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':''}))
    class Meta:
        model = Profile
        fields = ('nome', 'RG', 'CPF', 'sexo', 'foneFixo', 'foneCelular1', 'foneCelular2', 'foneCelular3',
                  'whatsapp','facebook','twitter','endereco','enderecoNumero','enderecoComplemento', 'estado',
                  'cidade','bairro','CEP','pergunta' )
        exclude = ('user', 'dataCadastro', 'cadastradoPor', 'ativo', 'pendente')


#FORMULARIO PARA TICKET
# class FormularioTicket(forms.ModelForm):
#     class Meta:
#         model = Ticket
#         fields = ('tickerUser', 'ticketDocumentoFiscal', 'ticketLocal')
#         exclude = ('ticketDataCriacao', 'ticketImpresso', 'ticketDataImpressao', 'ticketOperador')


class CepForm(forms.Form):
    cep =forms.CharField(label='CEP', max_length=9)
    endereco = forms.CharField(label='Endereço', widget=forms.Textarea, required=False)