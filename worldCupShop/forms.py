from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    pass


# formulaire d'ajout de programme
class AddProgrammeForm(forms.Form):
    label = forms.CharField(label='Titre', max_length=100)
    description = forms.CharField(label='Description', max_length=1000)
    thumbnail = forms.ImageField(label='Image')