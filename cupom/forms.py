from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cupom

class AddCupomForm(forms.Form):
    class Meta:
        model = Cupom
        fields = ('__all__')

class EditCupomForm(forms.Form):
    class Meta:
        model = Cupom
        fields = ('__all__')
        widgets = {
            'user': forms.HiddenInput,
        }
