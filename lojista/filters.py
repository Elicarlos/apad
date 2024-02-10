from django import forms
from django.contrib.auth.models import User, Group
from .models import Lojista
import django_filters

class LojistaFilter(django_filters.FilterSet):
    class Meta:
        model = Lojista
        fields = ['CNPJLojista', 'IELojista', 'razaoLojista', 'fantasiaLojista', 'ramoAtividade']
