# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError






#---------LOGIN------------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


#------------REGISTER-----------------

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                "class": "form-control"
            }
        ))
    
    adresse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Adresse",
                "class": "form-control"
            }
        ))
    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Telephone",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmer mot de passe",
                "class": "form-control"
            }
        ))
        

    class Meta:
        model = User
        fields = ('username', 'adresse', 'telephone' ,'email', 'password1', 'password2')


#---------------ADD LOCATAIRE---------------

class addLocataireForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    adresse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    date_joined = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "",
                "name":"datepicker" ,
                "class":"datepicker-default form-control",
                  
            }
        ))
    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
        

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name',
                  'date_joined','adresse', 'telephone' ,
                  'email', 'password1', 'password2')








#--------EDIT LOCATAIRE--------------


class editLocataireForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
              
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    adresse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    date_joined = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "",
                "name":"datepicker" ,
                "class":"datepicker-default form-control",
                  
            }
        ))
    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
        

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name',
                  'date_joined','adresse',
                   'telephone' ,'email', 'password1', 'password2')




#---------ADD GERANT---------------


class addGerantForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    

    adresse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    

    date_joined = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "",
                "name":"datepicker" ,
                "class":"datepicker-default form-control",
                  
            }
        ))
    

    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    signature = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
        

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','date_joined','adresse', 'telephone' ,'email', 'password1', 'password2','signature')



#--------EDIT GERANT-------------

class editGerantForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
              
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    adresse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    date_joined = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "",
                "name":"datepicker" ,
                "class":"datepicker-default form-control",
                  
            }
        ))
    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
        

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name',
                  'date_joined','adresse',
                   'telephone' ,'email', 'password1', 'password2')
        


class addAppForm(forms.ModelForm):
    nomAP = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"})
    )
    telAP = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"})
    )
    adresseAP = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "", "class": "form-control"})
    )
    nb_chambres = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "", "class": "form-control"})
    )
    nb_salles_bains = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "", "class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "", "class": "form-control"})
    )
    Gerant = forms.ModelChoiceField(
        queryset=Gerant.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    categorie = forms.ChoiceField(
        choices=Appartement.CATEGORIE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    image1 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    image2 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    image3 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Appartement
        fields = ('nomAP', 'telAP', 'adresseAP',
                   'nb_chambres', 'nb_salles_bains',
                     'description', 'Gerant', 'prix','image','image1','image2','image3','categorie')
        


#-------RESERVATION--------
class ReservationForm(forms.ModelForm):

    locataire = forms.ModelChoiceField(queryset=Locataire.objects.all(), label="Locataire")
    appartement = forms.ModelChoiceField(queryset=Appartement.objects.all(), label="Appartement")
    

    class Meta:
        model = Reservation
        fields = ['locataire', 'appartement', 'date_debut', 'date_fin', 'statut', 'frais']

class ReservationForm2(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        if date_debut and date_fin and date_debut >= date_fin:
            raise ValidationError("La date de début doit être avant la date de fin.")
        
        return cleaned_data

class ReservationMoisForm(forms.ModelForm):
    class Meta:
        model = ReservationMoi
        fields = ['date_debut', 'jour_payement', 'signature_locataire', 'methode_payement']
    
    def clean_jour_payement(self):
        jour_payement = self.cleaned_data['jour_payement']
        if jour_payement < 1 or jour_payement > 30:
            raise ValidationError("Le jour de paiement doit être compris entre 1 et 30.")
        return jour_payement

class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['statut']

class ReservationMoiStatusForm(forms.ModelForm):
    class Meta:
        model = ReservationMoi
        fields = ['statut']



class PayementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['numero_telephone', 'numero_de_transfert', 'capture_ecran']
        widgets = {
            'numero_telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_de_transfert': forms.TextInput(attrs={'class': 'form-control'}),
            'capture_ecran': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }