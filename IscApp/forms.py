from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Etudiant, Enseignant, Resultat, Promotion,UE
from django.contrib.auth import get_user_model

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)


class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['nom','postnom','prénom','adressephysique', 'email','telephone','motdepasse']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('nom', 'password')  # Should be username and password


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Identifiant',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre identifiant'})
    )
    password = forms.CharField(
        label='Mot de Passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )


class EtudiantCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = []

    def clean_matricule(self):
        matricule = self.cleaned_data.get('matricule')
        if Etudiant.objects.filter(matricule=matricule).exists():
            raise ValidationError("Ce numéro de matricule existe déjà.")
        return matricule


class EtudiantLoginForm(AuthenticationForm):
    username = forms.CharField(label="Matricule", max_length=20)

    def confirm_login_allowed(self, user):
        if not hasattr(user, 'etudiant_profile'):
            raise ValidationError("Seuls les étudiants sont autorisés à se connecter ici.")


class EtudiantRegistrationForm(forms.ModelForm):
    
    # Fields for CustomUser
    nom = forms.CharField(label="Nom")
    postnom = forms.CharField(label="PostNom")
    prénom = forms.CharField(label="Prénom")
    adressephysique = forms.CharField(label="AdressePhysique")
    email = forms.EmailField(label="Email")
    motdepasse = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    telephone = forms.CharField(label="Téléphone")

    PROMOTION_CHOICES = [('L1', 'Licence 1'), ('L2', 'Licence 2'), ('L3', 'Licence 3'), 
                         ('M1', 'Master 1'), ('M2', 'Master 2')]

    promotion = forms.ChoiceField(choices=PROMOTION_CHOICES, required=True, label="Promotion")

    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    SECTION_CHOICES = [('INFORMATIQUE', 'INFORMATIQUE'), ('COMPTABILITE', 'COMPTABILITE'),
                       ('DUANE', 'DUANE'), ('MARKETING', 'MARKETING'), ('BANQUE', 'BANQUE'),
                       ('COMMERCE EXTERIEUR', 'COMMERCE EXTERIEUR'), ('FISCALITE', 'FISCALITE'),
                       ('MANAGEMENT', 'MANAGEMENT'), ('AUTRE', 'AUTRE A préciser')]

    sexe = forms.ChoiceField(choices=SEXE_CHOICES, widget=forms.RadioSelect)
    option_section = forms.ChoiceField(choices=SECTION_CHOICES)
    
    class Meta:
        model = Etudiant
        fields = ['matricule', 'promotion', 'sexe', 'option_section', 'lieu_naissance', 'date_naissance', 'nationalite', 'profile_picture']

    def save(self, commit=True):
        # Create the CustomUser instance
        user = CustomUser(
            email=self.cleaned_data['email'],
            is_active=False,
            is_etudiant=True
        )
        user.set_password(self.cleaned_data['motdepasse'])
        user.save()

        # Create the Etudiant instance
        etudiant = super().save(commit=False)
        etudiant.user = user  # Link to the CustomUser
        if commit:
            etudiant.save()

        return etudiant


class EnseignantLoginForm(AuthenticationForm):
    username = forms.CharField(label="Numéro Employé", max_length=10)

    def confirm_login_allowed(self, user):
        if not hasattr(user, 'enseignant_profile'):
            raise forms.ValidationError("Seuls les enseignants sont autorisés à se connecter ici.")

    def confirm_login_allowed(self, user):
        if not user:
           raise forms.ValidationError("Seul l'enseignant est autorisé.")

class EnseignantRegistrationForm(forms.ModelForm):
    # Fields for CustomUser
    nom = forms.CharField(label="Nom")
    postnom = forms.CharField(label="PostNom")
    prénom = forms.CharField(label="prénom")
    adressephysique= forms.CharField(label="adressephysique")
    email = forms.EmailField(label="Email")
    motdepasse = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    telephone = forms.CharField(label="Telephone")

    PROMOTION_CHOICES = [('L1', 'Licence 1'), ('L2', 'Licence 2'), ('L3', 'Licence 3'), 
                         ('M1', 'Master 1'), ('M2', 'Master 2')]

    

    # Fields for Enseignant
    promotion = forms.ChoiceField(choices=PROMOTION_CHOICES, required=True, label="Promotion")

    class Meta:
        model = Enseignant
        fields = ['numero_employe', 'specialite', 'option_section', 'profile_picture']

    def save(self, commit=True):
        # Create the CustomUser instance
        user = CustomUser.objects.create(
            email=self.cleaned_data['email'],
            is_active=False,
            user_type='enseignant'
        )
        user.set_password(self.cleaned_data['motdepasse'])
        user.save()

        # Create the Enseignant instance
        enseignant = super().save(commit=False)
        enseignant.user = user  # Link to the CustomUser
        enseignant.numero_employe = generate_numero_employe()  # Function to generate numero_employe
        enseignant.save()

        return enseignant

# concernet etudiants

class ResultatForm(forms.ModelForm):
    class Meta:
        model = Resultat
        fields = [
            'etudiant', 'ue', 'semestre', 'matiere', 'categorie', 'credit',
            'cote', 'credits_capitalises', 'notes', 'travail_pratique',
            'interrogation', 'examen', 'validation', 'mention'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'validation': forms.Select(choices=[('Validé', 'Validé'), ('Non validé', 'Non validé')]),
        }


# concerne l'Enseignant
class Grille_de_coteForm(forms.ModelForm):
    etudiant = forms.ModelChoiceField(
        queryset=Etudiant.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionner un étudiant",
        label="Étudiant (Matricule)"
    )
    UE = forms.ModelChoiceField(
        queryset=UE.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionner une unité d'enseignement",
        label="Unité d'Enseignement"
    )
    promotion = forms.ModelChoiceField(
        queryset=Promotion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Sélectionner une promotion",
        label="Promotion"
    )
    credits = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 0}),
        label="Crédits"
    )

    class Meta:
        model = Resultat
        fields = ['etudiant', 'ue', 'promotion', 'credits', 'travail_pratique', 'interrogation', 'examen']
        widgets = {
            'travail_pratique': forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'interrogation': forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'examen': forms.NumberInput(attrs={'min': 0, 'max': 20}),
        }

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom d\'utilisateur'})
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )

    def confirm_login_allowed(self, user):
        if not user.is_superuser:
            raise ValidationError("Seuls les administrateurs peuvent se connecter ici.")



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['matricule', 'profile_picture']