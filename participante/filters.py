from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile, DocumentoFiscal
import django_filters

class UserFilter(django_filters.FilterSet):
    # first_name = django_filters.CharFilter(lookup_expr='icontains')
    # year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')

    class Meta:
        model = Profile
        fields = ['nome', 'CPF', 'RG', 'endereco']
        exclude = ['Email', 'photo']

class DocFilter(django_filters.FilterSet):
    class Meta:
        model = DocumentoFiscal
        fields = ['numeroDocumento', 'lojista', 'dataDocumento', 'valorDocumento', 'vendedor', 'status']

