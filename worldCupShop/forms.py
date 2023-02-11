from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    pass


# formulaire d'ajout de programme
class AddProgrammeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    label = forms.CharField(label='Titre', max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, label='Description', max_length=1000)
    thumbnail = forms.ImageField(label='Image (facultatif)', required=False)


# formulaire d'ajout de ligne d'exercice
class AddExerciceLineForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    # exercice = forms.CharField(label='Exercice', max_length=100)
    label = forms.CharField(label='Titre', max_length=100)
    nbSerie = forms.IntegerField(label='Nombre de série')
    # nbRepetition = forms.IntegerField(label='Nombre de répétition')
