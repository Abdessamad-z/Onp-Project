from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .validators import *


def myfilefield():
    return forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/pdf,image/*', "class": "form-control"}),
                           validators=[validate_file_extension, validate_type], required=True)



class CreatUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NavireForm(forms.Form):
    matricule = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    acte_de_nationalite = myfilefield()
    armateur_ou_RC = myfilefield()
    acte_cession_delegation = myfilefield()
    divers_documents = myfilefield()


class MareyeurForm(forms.Form):
    code_national = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    cin_mareyeur=myfilefield()
    rc_ou_statut = myfilefield()
    acte_de_cession = myfilefield()
    carte_marayeur_ou_autorisation = myfilefield()
    divers_documents = myfilefield()


class DocumentDetailsForm(forms.Form):
    file = myfilefield()
    delete = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.id = str(kwargs.pop('id'))
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update(
            {"id": "file_" + self.id, "onchange": "changeDate(this)"})
        self.fields['delete'].widget.attrs.update(
            {"id": "checkbox_" + self.id, "onchange": "myRemoveRow(this)"})
