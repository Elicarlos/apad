from calendar import month
from datetime import datetime
from decimal import Decimal
from io import BytesIO
import os
import json
from django.core.files import File
from pydoc import Doc
from unicodedata import decimal
from unittest import result
from django.http import HttpResponse, HttpResponseBadRequest, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from yaml import DocumentEndEvent
from .forms import *
from .models import Profile, DocumentoFiscal, Transacao
from lojista.models import Lojista
from .filters import UserFilter, DocFilter
from django.db.models.functions import Lower, Upper
from cupom.forms import AddCupomForm
from cupom.models import Cupom
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db import transaction
from .forms import LoginForm, CepForm
import requests
from django.contrib.auth.models import Group
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



import qrcode

import crcmod
import qrcode
import os


class Payload():
    def __init__(self, nome, chavepix, valor, cidade, txtId, diretorio=''):
        
        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor.replace(',', '.')
        self.cidade = cidade
        self.txtId = txtId
        self.diretorioQrCode = diretorio

        self.nome_tam = len(self.nome)
        self.chavepix_tam = len(self.chavepix)
        self.valor_tam = len(self.valor)
        self.cidade_tam = len(self.cidade)
        self.txtId_tam = len(self.txtId)

        self.merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{self.chavepix_tam:02}{self.chavepix}'
        self.transactionAmount_tam = f'{self.valor_tam:02}{float(self.valor):.2f}'

        self.addDataField_tam = f'05{self.txtId_tam:02}{self.txtId}'

        self.nome_tam = f'{self.nome_tam:02}'

        self.cidade_tam = f'{self.cidade_tam:02}'

        self.payloadFormat = '000201'
        self.merchantAccount = f'26{len(self.merchantAccount_tam):02}{self.merchantAccount_tam}'
        self.merchantCategCode = '52040000'
        self.transactionCurrency = '5303986'
        self.transactionAmount = f'54{self.transactionAmount_tam}'
        self.countryCode = '5802BR'
        self.merchantName = f'59{self.nome_tam:02}{self.nome}'
        self.merchantCity = f'60{self.cidade_tam:02}{self.cidade}'
        self.addDataField = f'62{len(self.addDataField_tam):02}{self.addDataField_tam}'
        self.crc16 = '6304'

  
    def gerarPayload(self):
        self.payload = f'{self.payloadFormat}{self.merchantAccount}{self.merchantCategCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'

        return self.gerarCrc16(self.payload)

    
    def gerarCrc16(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

        self.crc16Code = hex(crc16(str(payload).encode('utf-8')))

        self.crc16Code_formatado = str(self.crc16Code).replace('0x', '').upper().zfill(4)

        self.payload_completa = f'{payload}{self.crc16Code_formatado}'

        return self.payload_completa

    
    def gerarQrCode(self, payload, diretorio):
        dir = os.path.expanduser(diretorio)
        self.qrcode = qrcode.make(payload)
        self.qrcode.save(os.path.join(dir, 'pixqrcodegen.png'))
        
        return print(payload)





def not_found_page_view(request, exception):
    data = {}
    return render(request, 'not_found.html', data)

def server_error_view(request, exception):
    data = {}
    return render(request, 'not_found.html', data)

def main_page(request):
    login_form = LoginForm()
    return render(request, 'participante/coming_soon.html', {'section': 'homepage', 'lf': login_form})

#backoffice
@login_required
@user_passes_test(lambda u: u.is_staff)
def backoffice(request):
    docs_list = DocumentoFiscal.objects.filter(pendente=True).order_by('-dataCadastro')
    docs_list = Paginator(docs_list, 100)
    page = docs_list.page(request.GET.get('page', '1'))
    return render(request, 'participante/participante_backoffice.html', {'section': 'backoffice', 'docs': page})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def search(request):
      user_list = Profile.objects.all().order_by(Upper('nome').asc())
      user_filter = UserFilter(request.GET, queryset=user_list)
      return render(request, 'participante/participante_list.html', {'filter': user_filter,
                                                                     'section': 'participantes'})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def search_by_cpf(request):
    if(request.GET.get('q')):
        if 'q' in request.GET is not None:
            cpf = request.GET.get('q')
            # profile = get_object_or_404(Profile, CPF=cpf)
            # user = get_object_or_404(User, username= profile.user.username)
            try:
                # user = User.objects.get(username=cpf)
                profile = Profile.objects.get(CPF=cpf)
                if profile:
                    docs = DocumentoFiscal.objects.filter(user=profile.user)
                    return render(request, 'participante/detail.html', {'section': 'people','user': profile, 'docs': docs})
            except Profile.DoesNotExist:
                messages.error(request, 'Participante não cadastrado no sistema')
                return render(request, 'participante/search_by_cpf.html')
        else:
            messages.error(request, 'CPF não encontrado!')
    return render(request, 'participante/search_by_cpf.html')

def participante_list(request):
    f = ParticipanteFilter(request.GET, queryset=Profile.objects.all())
    return render(request, 'participante/template.html', {'filter': f})


@login_required
@transaction.atomic
def register2(request):
    if request.method == 'POST':
        try:
            usuario_aux = User.objects.get(username=request.POST['username'])
            if usuario_aux:
                messages.error(request, 'Não foi possivel prosseguir! Já existe um participante com este CPF ou Email cadastrado!')
                user_form = UserRegistrationForm()
                profile_form = ProfileRegistrationForm()
            return render(request, 'participante/register.html', {'user_form': user_form, 'profile_form': profile_form})

        except User.DoesNotExist:
            user_form = UserRegistrationForm(request.POST)
            profile_form = ProfileRegistrationForm(request.POST,
                                                  files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the User object
                new_user.save()
                # Create the user profile
                new_profile = profile_form.save(commit=False)
                new_profile.user = new_user
                new_profile.save()
                messages.success(request, 'Participante cadastrado com sucesso!')
                return render(request,
                              'participante/register_done2.html',
                              {'new_user': new_profile})
    else:
         user_form = UserRegistrationForm()
         profile_form = ProfileRegistrationForm()
    return render(request, 'participante/register.html', {'user_form': user_form, 'profile_form': profile_form})



def homepage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active and user.is_superuser:
                    login(request, user)                    
                    # return render(request, 'lojista/dashboard.html')
                    return redirect('lojista:homepage')   
                elif user.is_active:
                    login(request, user)
                    return redirect('participante:dashboard')                    
                    # return render(request, 'participante/dashboard.html')         
            else:
                login_form = LoginForm()
                return render(request, 'participante/index.html', {'section': 'homepage', 'lf': login_form})
    else:
        login_form = LoginForm()
    
    # return render(request, 'participante/coming_soon.html', {'section': 'homepage', 'lf': login_form})
    return render(request, 'participante/index.html', {'section': 'homepage', 'lf': login_form})

@login_required
def processar_checkout_post(nome_usuario, valor_total, codigo_transacao ):
    """
    Processa o checkout para o método POST.
    """

    qr_code_path = settings.QR_CODE_DIR
    payload = Payload(nome_usuario, 'ffc5effd-f33d-4959-b115-da3e9954c1a4', valor_total, 'Teresina', codigo_transacao, qr_code_path)
    return payload.gerarPayload()

@login_required
def checkout(request):
    if request.method == 'POST': 
        
        return render(request, 'participante/checkout.html')

    # Se não for um método POST, trata-se de um GET
   
    return render(request, 'participante/checkout.html')

@login_required
def pagamento(request):
    if request.method == "POST":
        print('Estou dentro do post')
        try:
            usuario = request.user
            nome_usuario = request.user.profile.nome
            total = request.POST.get('total')
            quantidade = request.POST.get('quantidade')

            # print("Total>>>>", total)
            # print("Quantidade>>>>", quantidade)

            

            # # Valide os dados do formulário
            # if total is None or quantidade is None:
            #     raise ValueError("Campos de formulário ausentes")

            total_convertido = float(total.replace('.', ','))
            quantidade_convertida = int(quantidade)

            # Verifique se já existe uma transação não processada para o usuário
            transacao_existente = Transacao.objects.filter(user=usuario, processada=False).first()

            if transacao_existente:
                # Atualiza a transação existente (se necessário)
                transacao_existente.valor_total = "{:.2f}".format(total_convertido)
                transacao_existente.save()
            else:
                # Senão, cria uma nova transação
                transacao = Transacao(user=usuario, valor_total="{:.2f}".format(total_convertido), quantidade_cupons=quantidade_convertida)
                transacao.save()
                
                codigo_transacao = transacao.id

                # Gere o QR code a partir do payload
                payload = Payload(nome_usuario, 'ffc5effd-f33d-4959-b115-da3e9954c1a4', "{:.2f}".format(total_convertido), 'Teresina', str(codigo_transacao))
                resultado_payload = payload.gerarPayload()
                # print('Resulado', resultado_payload)

                transacao.payload = resultado_payload
                transacao.save()

                qr_code_data = resultado_payload

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_code_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                img_io = BytesIO()
                img.save(img_io)
                transacao.qrcode.save(f'qrcode_{codigo_transacao}.png', File(img_io))

               
                # Redirecione para a página de confirmação
                return redirect('participante:confirmacao_pagamento', transacao_id=transacao.id)

        except ValueError as ve:
            print(f"Erro de validação: {str(ve)}")
            return HttpResponseBadRequest("Erro de validação: Campos de formulário ausentes ou inválidos")

        except Exception as e:
            print(f"Erro: {str(e)}")

    # Se ocorrer um erro ou a requisição não for POST, você pode redirecionar para outra página ou retornar uma resposta adequada
    return render(request, 'participante/pagina_de_erro.html')  # Substitua 'pagina_de_erro.html' pela página desejada
                   

                    
                    

               
            

def confirmacao_pagamento(request, transacao_id):
    # Recupere a transação com base no ID fornecido
    transacao = Transacao.objects.get(id=transacao_id)

    # Renderize a página que mostra o QR Code e o payload
    contexto = {'transacao': transacao}
    return render(request, 'participante/confirmacao_pagamento.html', contexto)


   
   

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Autenticado com sucesso!')
                else:
                    return HttpResponse('Conta desativada!')
            else:
                return HttpResponse('Login inválido!')
    else:
        form = LoginForm()
    return render(request, 'participante/login.html', {'form': form})

@transaction.atomic
def register(request):
    if request.method == 'POST':
        try:
            usuario_aux = User.objects.get(username=request.POST['username'])
            usuario_email = User.objects.get(email=request.POST['email'])
            if usuario_aux or usuario_email:
                messages.error(request, 'Erro! Já existe um usuário com o mesmo e-mail')
                user_form = UserRegistrationForm()
                profile_form = ProfileRegistrationForm()
            return render(request, 'participante/registerpart.html', {'user_form': user_form, 'profile_form': profile_form})

        except User.DoesNotExist:
            user_form = UserRegistrationForm(request.POST)
            profile_form = ProfileRegistrationForm(request.POST, files=request.FILES)

            if user_form.is_valid() and profile_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)               

                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the User object
                new_user.save()
                # Create the user profile
                new_profile = profile_form.save(commit=False)
                
                new_profile.CPF = user_form.cleaned_data['username']

                new_profile.user = new_user
                new_profile.save()
                # subject = "Cadastro concluido com sucesso! Liquida Teresina 2023"
                # body = "Seu cadastro na promoção Liquida Teresina 2023 foi realizado com sucesso!"
                # email = EmailMessage(subject, body, to=[new_user.email])
                # email.send()
                return render(request,
                              'participante/register_done.html',
                              {'new_user': new_profile})

            print("Form invalido")
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'participante/registerpart.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso')
            return render(request, 'participante/dashboard.html')
        else:
            messages.error(request, 'Erro na atualização do perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'participante/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, id):
    user = get_object_or_404(User, id=id, is_active=True)
    profile = get_object_or_404(Profile, user=user)
    docs_list = DocumentoFiscal.objects.filter(user=user)
    return render(request, 'participante/detail.html', {'section': 'people','user': profile, 'docs': docs_list})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def print_detail(request):
    docs_list = DocumentoFiscal.objects.filter(pendente=False, status=True).order_by('-dataCadastro')
    docs_list = Paginator(docs_list, 100)
    page = docs_list.page(request.GET.get('page', '1'))
    return render(request, 'participante/print_detail.html', {'section': 'people', 'docs': page})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def user_edit(request, id):
    if request.method == 'POST':
        instance_user = get_object_or_404(User, id=id)
        instance_profile = get_object_or_404(Profile, user=instance_user)
        profile_form = ProfileEditForm(instance=instance_profile,
                                        data=request.POST,
                                        files=request.FILES)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Participante validado com sucesso')
        else:
            messages.error(request, 'Erro na validação do Participante')
    else:
        instance_user = get_object_or_404(User, id=id)
        instance_profile = get_object_or_404(Profile, user=instance_user)
        profile_form = ProfileEditForm(instance=instance_profile)
    return render(request, 'participante/editbyoperador.html', {'profile_form': profile_form})

@login_required
@transaction.atomic
def adddocfiscal(request):
    

    if request.method == 'POST':
        documentoFiscal_form = UserAddFiscalDocForm(request.POST,
                                                    files=request.FILES)        
        
        # cnpj = documentoFiscal_form['lojista_cnpj'].value()
        cnpj = '10.570.679/0001-08'
               

        try:
            lojista = Lojista.objects.get(CNPJLojista=cnpj)
            user = request.user
            if lojista:
                if documentoFiscal_form.is_valid():
                    # Create a new document object but avoid saving it yet
                    new_documentoFiscal = documentoFiscal_form.save(commit=False)
                    # Set the user
                    new_documentoFiscal.user = user
                    new_documentoFiscal.lojista = lojista
                    new_documentoFiscal.valorDocumento = documentoFiscal_form.cleaned_data.get('valorDocumento')
                    # Save the doc object
                    new_documentoFiscal.save()
                    messages.success(request, 'Documento adicionado com sucesso!')
                    return render(request,
                                  'participante/doc_fiscal_done.html',
                                  {'new_documentoFiscal': new_documentoFiscal})
        except Lojista.DoesNotExist:
            messages.error(request, "Lojista não cadastrado na base de dados <a href='https://wa.me/5586999950081?text=Ola%20preciso%20de%20suporte' style='color: #FFF'>     <b> |Informar ao Suporte|</b></a>")
            documentoFiscal_form = UserAddFiscalDocForm()
            return render(request, 'participante/doc_fiscal_add.html', {'documentoFiscal_form': documentoFiscal_form})
    else:
        documentoFiscal_form = UserAddFiscalDocForm()
    return render(request, 'participante/doc_fiscal_add.html', {'documentoFiscal_form': documentoFiscal_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def adddocfiscalbyop(request, id):
    user = get_object_or_404(User, id=id)
    is_superuser = request.user.is_superuser
    
    if request.method == 'POST':
        try:
            user_aux = User.objects.get(id=id)
            if is_superuser:
                documentoFiscal_form = UserAddFiscalDocFormSuperuser(request.POST, files=request.FILES)
            else:
                documentoFiscal_form = UserAddFiscalDocForm(request.POST, files=request.FILES)
            
            cnpj = documentoFiscal_form['lojista_cnpj'].value()
            numerodoc = documentoFiscal_form['numeroDocumento'].value()
            lojista = Lojista.objects.get(CNPJLojista=cnpj)
            
            if user_aux or lojista:
                if documentoFiscal_form.is_valid():
                    new_documentoFiscal = documentoFiscal_form.save(commit=False)
                    new_documentoFiscal.user = user_aux
                    new_documentoFiscal.lojista = lojista
                    new_documentoFiscal.save()

                    return render(request,
                                  'participante/doc_fiscal_done_op.html',
                                  {'new_documentoFiscal': new_documentoFiscal, 'participante': user_aux})
                else:
                    messages.error(request, 'Ops! Parece que algo não está certo. Verifique se todas as informações estão corretas!')
            else:
                messages.error(request, 'Algo deu errado com o usuário ou lojista.')
        except Lojista.DoesNotExist:
            messages.error(request, 'O lojista do documento ainda não se encontra na nossa base de dados!')
            documentoFiscal_form = UserAddFiscalDocForm()
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e}')
            documentoFiscal_form = UserAddFiscalDocForm()
    else:
        if is_superuser:
            documentoFiscal_form = UserAddFiscalDocFormSuperuser()
        else:
            documentoFiscal_form = UserAddFiscalDocForm()
    
    return render(request, 'participante/doc_fiscal_add_op.html', {'documentoFiscal_form': documentoFiscal_form, 'participante': user})
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def adddocfiscalbyop(request, id):
#     user = get_object_or_404(User, id=id)
#     if request.method == 'POST':
#         documentoFiscal_form = UserAddFiscalDocForm(request.POST,
#                                                     files=request.FILES)
#         cnpj = documentoFiscal_form['lojista_cnpj'].value()
#         numerodoc = documentoFiscal_form['numeroDocumento'].value()
#         if cnpj:
#             lojista = get_object_or_404(Lojista, CNPJLojista=cnpj)
#             user = get_object_or_404(User, id=id)
#             if documentoFiscal_form.is_valid():
#                 # Create a new document object but avoid saving it yet
#                 new_documentoFiscal = documentoFiscal_form.save(commit=False)
#                 # Set the user
#                 new_documentoFiscal.user = user
#                 new_documentoFiscal.lojista = lojista
#                 # Save the doc object
#                 new_documentoFiscal.save()
#                 return render(request,
#                               'participante/doc_fiscal_done_op.html',
#                               {'new_documentoFiscal': new_documentoFiscal, 'participante': user})
#             else:
#                 messages.error(request, 'O documento {} já se encontra cadastrado na nossa base de dados!'.format(numerodoc))
#         else:
#             messages.error(request, 'O lojista do documento ainda não se encontra na nossa base de dados!')
#     else:
#         user = get_object_or_404(User, id=id)
#         documentoFiscal_form = UserAddFiscalDocForm()
#     return render(request, 'participante/doc_fiscal_add_op.html', {'documentoFiscal_form': documentoFiscal_form, 'participante': user})

@login_required
def doclist(request):
    docs_list = DocumentoFiscal.objects.filter(user=request.user)
    docs_filter = DocFilter(request.GET, queryset=docs_list)
    return render(request, 'participante/list_doc_fiscal.html', {'filter': docs_filter,
                                                                   'section':'docsfiscais'})

@login_required
@transaction.atomic
def editdocfiscal(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(DocumentoFiscal, id=id)
        documentofiscal_form = DocumentoFiscalEditForm(instance=instance,
                                                                        data=request.POST,
                                                                        files=request.FILES)
        if documentofiscal_form.is_valid():
            new_doc = documentofiscal_form.save(commit=False)
            new_doc.observacao = "Nenhuma"
            new_doc.save()
            messages.success(request, 'Documento Fiscal atualizado com sucesso!')
        else:
            messages.error(request, 'Erro na atualização do documento Fiscal! verifique se não há algum dado incoerênte no formulario')
    else:
        instance = get_object_or_404(DocumentoFiscal, id=id)
        documentofiscal_form = DocumentoFiscalEditForm(instance=instance)
    return render(request, 'participante/doc_fiscal_edit.html', {'documentofiscal_form': documentofiscal_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def editdocfiscalbyop(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(DocumentoFiscal, id=id)
        documentofiscal_form = DocumentoFiscalEditFormOp(instance=instance,
                                                                        data=request.POST,
                                                                        files=request.FILES)
        if documentofiscal_form.is_valid():
            documentofiscal_form.save()
            messages.success(request, 'Documento Fiscal atualizado com sucesso!')
        else:
            messages.error(request, 'Erro na atualização do documento Fiscal! verifique se não há algum dado incoerênte no formulario')
    else:
        instance = get_object_or_404(DocumentoFiscal, id=id)
        documentofiscal_form = DocumentoFiscalEditFormOp(instance=instance)
    return render(request, 'participante/doc_fiscal_edit.html', {'documentofiscal_form': documentofiscal_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
@transaction.atomic
def validadocfiscal(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(DocumentoFiscal, id=id)
        documentofiscal_form = DocumentoFiscalValidaForm(instance=instance,data=request.POST,
                                                                    files=request.FILES)
        profile = get_object_or_404(Profile, user= instance.user)
        docs = DocumentoFiscal.objects.filter(user=instance.user)
        pendente = documentofiscal_form['pendente'].value()
        if documentofiscal_form.is_valid() and not pendente:
            new_doc = documentofiscal_form.save(commit=False)
            new_doc.qtde = int(new_doc.get_cupons())
            new_doc.status = True
            impressaoHab = True
            new_doc.save()
            # ticket = Ticket(User, user=instance.user)
            # print(ticket)
            if not new_doc.pendente:
                for x in range(new_doc.qtde):
                    cupom = Cupom.objects.create(documentoFiscal=new_doc, user=new_doc.user, operador=request.user)
            # subject = "Você já está concorrendo! Liquida Teresina 2023"
            # body = "Seus cupons já foram validados e impressos agora é só aguardar o sorteio"
            # email = EmailMessage(subject, body, to=[new_doc.user.email])
            # email.send()
            # messages.success(request, 'Documento Fiscal validado com sucesso, agora você pode Imprimir os cupons')
            return render(request, 'participante/detail.html', {'section': 'people','user': profile, 'docs': docs})
        elif documentofiscal_form.is_valid() and pendente:
            new_doc = documentofiscal_form.save(commit=False)
            # new_doc.status = False
            new_doc.save()

            messages.info(request, 'O documento fiscal {} não foi validado por pendencias. Se está tudo certo com o documento, por favor repita novamente o procedimento de validação e desmarque a opção de pendente para que o mesmo seja validado! Se você encontrou pendêcias no documento em questão por favor não esqueça de descriminar a pendência no campo obsevações!'.format(new_doc.numeroDocumento))
            return render(request, 'participante/detail.html', {'section': 'people','user': profile, 'docs': docs})
        else:
            messages.error(request, 'Ocorreu um erro durante o processo de validação verifique se não há algum dado incoerênte no formulario!')
    else:
        instance = get_object_or_404(DocumentoFiscal, id=id)
        documentofiscal_form = DocumentoFiscalValidaForm(instance=instance)
    return render(request, 'participante/doc_fiscal_valida.html', {'documentofiscal_form': documentofiscal_form, 'doc':instance})


@login_required
def dashboard(request):
    if request.user.is_superuser: return render(request, 'lojista/dashboard.html', {'section': 'lojista'})
    docs = DocumentoFiscal.objects.filter(user=request.user)
    return render(request, 'participante/dashboard.html', {'section': 'dashboard','docs': docs})

@login_required
def lojista(request):
    return render(request, 'not_found.html', {'section': 'coupons'})

@login_required
def coupons(request):
    return render(request, 'participante/coupons.html', {'section': 'coupons'})

@login_required
def premios(request):
    return render(request, 'participante/premios.html', {'section': 'premios'})

from django.db.models.functions import TruncMonth, TruncDate

from django.db.models.aggregates import Count, Avg, Min, Max, Sum
from django.db.models import Count, F

# from django.db.models.functions import ExtractDay, ExtractMonth, ExtractQuarter, ExtractIsoWeekDay, ExtractWeekDay, ExtractIsoYear, ExtractYear


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dados_campanha(request):
    quant_cupons = Cupom.objects.all().count()
    quant_usuario = Profile.objects.count()
    quant_lojistas = Lojista.objects.count()    
    quant_documentos = DocumentoFiscal.objects.count()
    # lojista = DocumentoFiscal.objects.select_related('lojista', 'user')

    labels = []
    data = []
    data_faturamento = []
    valor_faturamento = []
    # da = get_data(cupons)
    # print("Resultado da Funcao >>>>>>>>>>", data)
    # cup = Cupom.objects.values('dataCriacao').annotate(total=Count(data))
    bu = Cupom.objects.all().annotate(date=TruncDate('dataCriacao')).values('date').annotate(Count('dataCriacao')).order_by('date')
    faturamento_por_dia = DocumentoFiscal.objects.all().annotate(date=TruncDate('dataCadastro')).values('date').annotate(valor=Sum('valorDocumento')).order_by('date')
    # q1 = DocumentoFiscal.objects.select_related('user').annotate(total=Sum('valorDocumento'))

    # for q in q1:
    #     print('Cliente', q.user.profile.nome, 'Total', q.total)

    q1 = DocumentoFiscal.objects.all().select_related('user')
    q2 = q1.values('user__profile__CPF', 'user__profile__nome').annotate(total=Sum('valorDocumento'), virtual=Sum('valorVirtual'))
    q3 = q2.order_by('-total', '-user__profile__CPF')[:10]
    cliente_cpf = []
    total_cpf = []

    for q in q3:
        cliente_cpf.append(q['user__profile__CPF'])
        total = float(q['total'])
        total_cpf.append(total)

    
    

    cupons_por_operador = (
    Cupom.objects
    .values('operador__first_name')
    .annotate(cupom_count=Count('id'))
    .order_by('-cupom_count')
    )

    # Query para obter informações sobre os operadores, incluindo o first_name
    operadores_info = [
        {'operador': item['operador__first_name'], 'cupom_count': item['cupom_count']}
        for item in cupons_por_operador
    ]

    
    



    grupos = Group.objects.filter(name__in=["Teresina Shopping", "Riverside","Rio Poty", "Pintos Dirceu"])

    labels_grupo = []
    data_cupons_por_grupo = []

    for grupo in grupos:
        operadores_do_grupo = User.objects.filter(groups=grupo)
        cupons_por_grupo = Cupom.objects.filter(operador__in=operadores_do_grupo).count()
        labels_grupo.append(grupo.name)
        data_cupons_por_grupo.append(cupons_por_grupo)


       
        
    for fat in faturamento_por_dia:
        dt = fat['date']
        dt = datetime.strftime(dt,"%d/%m")
        data_faturamento.append(dt)
        fat = float(fat['valor'])        
        valor_faturamento.append(fat)



    for b in bu:
        dt = b['date']
        dt = datetime.strftime(dt,"%d/%m")        
        labels.append(dt)
        data.append(b['dataCriacao__count'])


    quant_doc_ramoAtividade = DocumentoFiscal.objects.all().select_related('lojista')
    query_ramoAtividade = quant_doc_ramoAtividade.values('lojista__ramoAtividade__atividade').annotate(total=Count('id'))
    ramo_atividade = []
    quant_ramo_atividade = []

   
    for q in query_ramoAtividade:
        # atividade = q['lojista__ramo__atividade']
        atividade = q['lojista__ramoAtividade__atividade']
        ramo_atividade.append(atividade)
        total = q['total']
        quant_ramo_atividade.append(total)     

    

    operadores = User.objects.filter(is_staff=True).count()
    faturamento_total = DocumentoFiscal.objects.aggregate(total=Sum('valorDocumento'))
    faturamento_total = faturamento_total['total']
    if faturamento_total is None:
        faturamento_total = 0
        ticket_medio = 0
    
    else:
        ticket_medio = float(faturamento_total / quant_documentos) 

  

    context = {
        'labels': labels,
        'data': data,      
        'data_faturamento': data_faturamento,
        'valor_faturamento': valor_faturamento,
        'ramo_atividade': ramo_atividade,
        'quant_ramo_atividade':quant_ramo_atividade,
        'cliente_cpf': cliente_cpf,
        'total_cpf': total_cpf,
        'operadores_info': operadores_info,
        'labels_grupo': labels_grupo,
        'data_cupons_por_grupo': data_cupons_por_grupo,
        'quant_cupons': quant_cupons,
        'quant_usuario': quant_usuario,
        'quant_lojistas': quant_lojistas,
        'quant_documentos': quant_documentos,
        'operadores': operadores,
        'faturamento_total': faturamento_total,
        'ticket_medio': ticket_medio,       
    }
    return render(request, 'dash/index.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def graficos(request):    
    labels = []
    data = []
    data_faturamento = []
    valor_faturamento = []
    # da = get_data(cupons)
    # print("Resultado da Funcao >>>>>>>>>>", data)
    # cup = Cupom.objects.values('dataCriacao').annotate(total=Count(data))
    bu = Cupom.objects.all().annotate(date=TruncDate('dataCriacao')).values('date').annotate(Count('dataCriacao')).order_by('date')
    faturamento_por_dia = DocumentoFiscal.objects.all().annotate(date=TruncDate('dataCadastro')).values('date').annotate(valor=Sum('valorDocumento')).order_by('date')
    # q1 = DocumentoFiscal.objects.select_related('user').annotate(total=Sum('valorDocumento'))

    # for q in q1:
    #     print('Cliente', q.user.profile.nome, 'Total', q.total)

    q1 = DocumentoFiscal.objects.all().select_related('user')
    q2 = q1.values('user__profile__CPF', 'user__profile__nome').annotate(total=Sum('valorDocumento'), virtual=Sum('valorVirtual'))
    q3 = q2.order_by('-total', '-user__profile__CPF')[:10]
    cliente_cpf = []
    total_cpf = []

    for q in q3:
        cliente_cpf.append(q['user__profile__CPF'])
        total = float(q['total'])
        total_cpf.append(total)

    
    cupons_por_operador = Cupom.objects.values('operador__username').annotate(cupom_count=Count('id'))
    operadores_info = [
        {'operador': item['operador__username'], 'cupom_count': item['cupom_count']}
        for item in cupons_por_operador
    ]



    grupos = Group.objects.filter(name__in=["Teresina Shopping", "Riverside"])

    labels_grupo = []
    data_cupons_por_grupo = []

    for grupo in grupos:
        operadores_do_grupo = User.objects.filter(groups=grupo)
        cupons_por_grupo = Cupom.objects.filter(operador__in=operadores_do_grupo).count()
        labels_grupo.append(grupo.name)
        data_cupons_por_grupo.append(cupons_por_grupo)


    



    
    
        
    for fat in faturamento_por_dia:
        dt = fat['date']
        dt = datetime.strftime(dt,"%d/%m")
        data_faturamento.append(dt)
        fat = float(fat['valor'])        
        valor_faturamento.append(fat)



    for b in bu:
        dt = b['date']
        dt = datetime.strftime(dt,"%d/%m")        
        labels.append(dt)
        data.append(b['dataCriacao__count'])


    quant_doc_ramoAtividade = DocumentoFiscal.objects.all().select_related('lojista')
    query_ramoAtividade = quant_doc_ramoAtividade.values('lojista__ramoAtividade__atividade').annotate(total=Count('id'))
    ramo_atividade = []
    quant_ramo_atividade = []

   
    for q in query_ramoAtividade:
        # atividade = q['lojista__ramo__atividade']
        atividade = q['lojista__ramoAtividade__atividade']
        ramo_atividade.append(atividade)
        total = q['total']
        quant_ramo_atividade.append(total)     

    
    
    print(operadores_info)
    

    context = {        
        'labels': labels,
        'data': data,      
        'data_faturamento': data_faturamento,
        'valor_faturamento': valor_faturamento,
        'ramo_atividade': ramo_atividade,
        'quant_ramo_atividade':quant_ramo_atividade,
        'cliente_cpf': cliente_cpf,
        'total_cpf': total_cpf,
        'operadores_info': operadores_info,
        'labels_grupo': labels_grupo,
        'data_cupons_por_grupo': data_cupons_por_grupo,
    
    }
    return render(request, 'dash/charts.html', context)




def relatorios_camp(request):    
    return render(request, 'dash/tables.html'  )



'''from utils.ticket import validarticket
#FUNCOES PARA GERACAO DE TICKETS
def gerarticket(request):
    return render(request, 'ticket/pages/home.html', context={
        'ticket': validarticket
    })'''


def consulta_cep(request):
    form = CepForm(request.POST or None)

    

    return render(request, 'participante/form.html', {'form': form})


def resumo_lojistas(request):
    # documento = Momde
    return render(request, 'dash/tables.html')
