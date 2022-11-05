from django import forms
from django.core import validators
from .models import Receta

class RecetaForm(forms.ModelForm):
    nombre = forms.CharField(validators=[validators.RegexValidator("^[A-Z]+")], error_messages={'invalid':"El nombre debe empezar por mayúscula"})
    preparación = forms.CharField(widget=forms.Textarea,validators=[validators.RegexValidator("^[A-Z]+")], error_messages={'invalid':"La preparación debe empezar por mayúscula"})

    class Meta:
        model = Receta
        fields = ('nombre','preparación',)