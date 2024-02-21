from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import AddCupomForm, EditCupomForm
from .models import Cupom
from bcp.views import print_qrcode
from participante.models import DocumentoFiscal
from django.db import transaction
import threading


gerarcupons_sem = threading.Semaphore()

@login_required
@user_passes_test(lambda u: u.is_superuser)
def detail(request):
    return render(request, 'cupom/detail.html', {'section': 'cupom-detail'})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addcupom(request, numerodocumento):
    if request.method == 'POST':
        cupom_form = AddCupomForm(request.POST)
        doc = get_object_or_404(DocumentoFiscal, numeroDocumento=numerodocumento)
        new_cupom = cupom_form.save(commit=False)
        new_cupom.documentoFiscal = doc
        new_cupom.user = doc.user
        new_cupom.operador = request.user
        new_cupom.save()
        messages.success(request, 'Cupom gerado com sucesso')
    else:
        messages.success(request, 'Erro ao gerar o cupom')
        
@login_required
@user_passes_test(lambda u: u.is_superuser)
def gerarcupons(request, numerodocumento):
    with gerarcupons_sem:       
        if request.method == 'POST':
            doc = get_object_or_404(DocumentoFiscal, numeroDocumento=numerodocumento)
            qtde = int(doc.get_cupons())

            cupons_gerados = []

            with transaction.atomic():
                for c in range(qtde):
                    novo_cupom = addcupom(request, numerodocumento)
                    if novo_cupom:
                        cupons_gerados.append(novo_cupom)

            if len(cupons_gerados) == qtde:
                messages.success(request, f'{qtde} cupons gerados com sucesso!')
            else:
                messages.error(request, 'Erro ao gerar cupons')

    return HttpResponse('/')
    

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cupomlist(request, username):
    user = get_object_or_404(User, username=username)
    cupons = Cupom.objects.filter(user)
    return render(request, 'cupom/list.html', {'section': 'cuponslist',
                                                      'cupons': cupons})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def printCupom(request, numerodocumento):
    doc_instance = get_object_or_404(DocumentoFiscal, numeroDocumento=numerodocumento )
    cupons = Cupom.objects.filter(doc_instance)
    for cupom in cupons:
        print_qrcode(request, cupom.get_token, numerodocumento)
