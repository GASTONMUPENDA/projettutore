# forms.py
from django . core import validators
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser,Etudiant,Enseignant




user = get_user_model()

class CustomUser(forms.ModelForm):
    
       class Meta(UserCreationForm.Meta):
           model = CustomUser
           fields = ['username', 'email' ]

class CustomAuthentication():
       class Meta:
        model = user
        fields = ('username', 'password')

          
        
# champs du fo  # Ajustez selon les champs de votre modèle
       

class EtudiantCreationForm(UserCreationForm):
    class Meta:
        model = Etudiant
        fields = ['nom','prénom', 'email', 'matricule', 'date_naissance', 'adressephysique', 'telephone', 'motdepasse']

class EtudiantLoginForm(AuthenticationForm):
    class Meta:
        model = Etudiant
        fields = ('matricule', 'motdepasse')


    
class EnseignantRegistration(forms.ModelForm):
        class Meta:
                model=Enseignant
                fields= ['numero_employe','email','motdepasse']
                widgets ={
                'numero_employe':forms.TextInput(attrs={'class':'form-control'}),
                'email':forms.EmailInput(attrs={'class':'form-control'}),
                'motdepasse':forms.PasswordInput(attrs={'class':'form-control'}),
         }

