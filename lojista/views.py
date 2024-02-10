from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from participante.forms import ProfileEditForm, UserEditForm
from .forms import LojistaRegistrationForm, RamoAtividadeRegistrationForm
from .models import Lojista, RamoAtividade
from django.contrib.auth.decorators import user_passes_test
from .filters import LojistaFilter
from django.db.models.functions import Lower, Upper
from cupom.models import Cupom
from participante.models import Profile
from django.contrib.auth.models import User
from participante.models import DocumentoFiscal
from django.core.exceptions import ObjectDoesNotExist

@login_required
@user_passes_test(lambda u: u.is_staff)
def reprint(request):
    if(request.GET.get('q')):
        if 'q' in request.GET is not None:
            cpf = request.GET.get('q')
            try:
                # user = User.objects.get(username=cpf)
                profile = Profile.objects.get(CPF=cpf)
                if profile:
                    docs = DocumentoFiscal.objects.filter(user=profile.user)
                    return render(request, 'participante/reprint.html', {'section': 'reeprint','docs': docs,'user': profile})
            except Profile.DoesNotExist:
                messages.error(request, 'Participante não cadastrado no sistema')
                return render(request, 'participante/search_by_doc.html')
        else:
            messages.error(request, 'Documento não encontrado!')
    return render(request, 'participante/search_by_doc.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cupons(request):
    if(request.GET.get('q')):
        if 'q' in request.GET is not None:
            cpf = request.GET.get('q')
            profile = get_object_or_404(Profile, CPF=cpf)
            user = get_object_or_404(User, username= profile.user.username)
            cupons = Cupom.objects.filter(user=user)
            return render(request, 'lojista/cupons.html', {'section': 'cupons','user': profile, 'cupons': cupons})
        else:
            messages.error(request, 'CPF não encontrado!')
    return render(request, 'lojista/search_by_cpf.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def search_cupom(request):
    if(request.GET.get('q')):
        if 'q' in request.GET is not None:
            numeroCupom = request.GET.get('q')
            # profile = get_object_or_404(Profile, CPF=cpf)
            # user = get_object_or_404(User, username= profile.user.username)
            # cupons = Cupom.objects.filter(user=user)
            try:
                cupom = Cupom.objects.get(id=numeroCupom)
                if cupom:
                    profile = Profile.objects.get(user=cupom.user)
                    return render(request, 'lojista/cupom_detail.html', {'section': 'cupons','user': profile, 'cupom': cupom})
            except Cupom.DoesNotExist:
                messages.error(request, 'Cupom não encontrado!')
                return render(request, 'lojista/search_by_cupom.html')
        else:
            messages.error(request, 'Cupom não encontrado!')
    return render(request, 'lojista/search_by_cupom.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def search(request):
      lojista_list = Lojista.objects.all().order_by(Upper('fantasiaLojista').asc())
      lojista_filter = LojistaFilter(request.GET, queryset=lojista_list)
      return render(request, 'lojista/lojistas_list.html', {'filter': lojista_filter,
                                                                     'section':'lojistas'})


def is_operador(user):
    return user.groups.filter(name='Operador').exists()

def is_gerente(user):
    return user.groups.filter(name='Gerente').exists()

def is_backoffice(user):
    return user.groups.filter(name='Backoffice').exists()

def is_supervisor(user):
    return user.groups.filter(name='Supervisor').exists()





@login_required
@user_passes_test(lambda u: u.is_superuser)
def homepage(request):
    context = {
        'section': 'lojista',
        'is_operador': is_operador(request.user),
        'is_gerente': is_gerente(request.user),
        'is_backoffice':is_backoffice(request.user),
        'is_supervisor': is_supervisor(request.user),
    }
    return render(request, 'lojista/dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def register(request):
    if request.method == 'POST':
        lojista_form = LojistaRegistrationForm(request.POST)
        if lojista_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_lojista = lojista_form.save(commit=False)
            # Save the User object
            new_lojista.save()
            return render(request,
                          'lojista/register_done.html',
                          {'new_lojista': new_lojista})

    else:
        lojista_form = LojistaRegistrationForm()
    return render(request, 'lojista/register.html', {'lojista_form': lojista_form   })

@login_required
@user_passes_test(lambda u: u.is_superuser)
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
        else:
            messages.error(request, 'Erro na atualização do perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'participante/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editlojista(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(Lojista, id=id)
        lojista_form = LojistaRegistrationForm(instance=instance,
                                                data=request.POST)
        if lojista_form.is_valid():
            lojista_form.save()
            messages.success(request, 'Perfil atualizado com sucesso')
        else:
            messages.error(request, 'Erro na atualização do Lojista')
    else:
        instance = get_object_or_404(Lojista, id=id)
        lojista_form = LojistaRegistrationForm(instance=instance)
    return render(request, 'lojista/edit.html', {'lojista_form': lojista_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def lojistalist(request):
    lojistas = Lojista.objects.all()
    return render(request, 'lojista/list_lojistas.html', {'section': 'listar-lojistas',
                                                      'lojistas': lojistas})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def registeratividade(request):
    if request.method == 'POST':
        ramoatividade_form = RamoAtividadeRegistrationForm(request.POST)

        if ramoatividade_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_ramoatividade = ramoatividade_form.save(commit=False)
            # Save the User object
            new_ramoatividade.save()
            return render(request,
                          'lojista/register_ramo_atividade_done.html',
                          {'new_ramoatividade': new_ramoatividade})
    else:
        ramoatividade_form = RamoAtividadeRegistrationForm()
    return render(request, 'lojista/register_ramo_atividade.html', {'ramoatividade_form': ramoatividade_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def listatividade(request):
    ramosatividade = RamoAtividade.objects.all()
    return render(request, 'lojista/list_ramo_atividade.html', {'section': 'ramoatividade',
                                                      'ramosatividade': ramosatividade})
