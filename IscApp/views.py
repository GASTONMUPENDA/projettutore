from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login , authenticate, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .forms import EtudiantCreationForm, EtudiantLoginForm,EtudiantRegistrationForm, CustomUserForm,ResultatForm,SearchForm
from django.contrib import admin,messages
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import CustomUserForm, EtudiantCreationForm, EtudiantLoginForm,EtudiantRegistrationForm,EnseignantLoginForm,EnseignantRegistrationForm, CustomUserForm,CustomLoginForm,Grille_de_coteForm,ProfileForm
from django.http import HttpResponseRedirect
from .models import CustomUser, Etudiant,Enseignant,UE,CustomUser,Promotion, Notification,Resultat
from django.conf import settings
from django.views.generic.edit import UpdateView
from django.template.loader import get_template,render_to_string
from django.utils import timezone
from .utils import generate_numero_employe
import feedparser
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from xhtml2pdf import pisa
from datetime import datetime
from .utils import send_email_with_html_body
import random 
import csv
from django.core.management.base import BaseCommand
from django.http import JsonResponse
from .models import Resultat

 



CustomUser = get_user_model()
def navbare(request):
    return render(request,IscApp/navbare.html)

def home(request):
    
    return render(request, 'IscApp/home.html')

@login_required
def UE(request):
    if request.user.is_Enseignat:
        UE = ue.objects.filter(Enseignant=request.user)
        return render(request, 'cours.html', {'cours': cours})
    else:
        messages.error(request, "Vous n'êtes pas autorisé à voir cette page.")
        return redirect('home')

@login_required
def cours_detail(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id, Enseignant=request.user)
    Etudiants = Etudiant.objects.filter(cours=cours)

    if request.method == 'POST':
        form = noteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.cours = cours
            note.save()
            messages.success(request, "Note ajoutée/modifiée avec succès.")
            return redirect('cours_detail', cours_id=cours_id)
    else:
        form = noteForm()

    return render(request, 'cours_detail.html', {'cours': cours, 'Etudiants': Etudiants, 'form': form})

def user_choice(request):
   
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'Etudiant':
         
         return redirect( 'login_Etudiant')
        elif user_type == 'Enseignant':
            return redirect('login_Enseignant')
            
    return render(request, 'IscApp/user_choice.html')

def register_Etudiant(request):
    if request.method == 'POST':
        etudiant_form = EtudiantRegistrationForm(request.POST, request.FILES)
        if etudiant_form.is_valid():
            try:
                # Vérifiez si l'adresse e-mail existe déjà
                if CustomUser.objects.filter(email=etudiant_form.cleaned_data['email']).exists():
                    etudiant_form.add_error('email', 'L\'adresse e-mail saisie existe déjà.')
                else:
                    # Créez l'utilisateur CustomUser
                    new_user = CustomUser.objects.create_user(
                        email=etudiant_form.cleaned_data['email'],
                        password=etudiant_form.cleaned_data['motdepasse'],
                        nom=etudiant_form.cleaned_data['nom'],
                        postnom=etudiant_form.cleaned_data['postnom'],
                        prénom=etudiant_form.cleaned_data['prénom'],
                        adressephysique=etudiant_form.cleaned_data['adressephysique'],
                        telephone=etudiant_form.cleaned_data['telephone']
                    )

                    # Créez et associez l'objet Etudiant
                    etudiant = etudiant_form.save(commit=False)
                    etudiant.user = new_user
                    etudiant.save()

                    # Envoi de notification à l'administrateur
                    notify_admin(sender=CustomUser, instance=etudiant, created=True)

                    # Message de succès
                    messages.success(request, "Étudiant enregistré avec succès. En attente de validation.")

                    # Connectez l'utilisateur après l'enregistrement
                    login(request, new_user)

                    # Redirigez vers le tableau de bord de l'étudiant
                    return redirect('IscApp:TableauDeBord')
            except Exception as e:
                messages.error(request, f"Une erreur s'est produite : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        etudiant_form = EtudiantRegistrationForm()

    return render(request, 'deroulement/register_Etudiant.html', {'form': etudiant_form})


def login_Etudiant(request):
    if request.method == 'POST':
        form = EtudiantLoginForm(request, data=request.POST)
        if form.is_valid():
            matricule = form.cleaned_data.get('username')  # Récupère le matricule saisi
            motdepasse = form.cleaned_data.get('password')  # Récupère le mot de passe saisi 
            user = authenticate(request, username=matricule, password=motdepasse)

            if user is not None and user.is_etudiant:
                login(request, user)
                return redirect('TableauDeBord')
        else:
             form.add_error(None, "Matricule ou mot de passe incorrect.")
        # Si l'utilisateur n'est pas un étudiant, afficher un message d'erreur

    else:
        form = EtudiantLoginForm(request, data=request.POST)
    return render(request, 'IscApp/login_Etudiant.html')  

def TableauDeBord(request):
    return render(request, 'IscApp/TableauDeBord.html') 

class registerEtudiantView(CreateView):
    model = Etudiant
    form_class =  EtudiantCreationForm
    template_name = 'IscApp/registration/register_Etudiant.html'
    success_url = reverse_lazy('login_Etudiant')

    def form_valid(self, form):
        form.instance.is_active =True #activer l'etudiant
        return super().form_valid(form)

class SignupView(CreateView):
    form_class = CustomUser
    template_name = 'IscApp/signup.html'
    
    success_url = reverse_lazy('register_Etudiant')
    

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form)


@login_required
def voir_resultats(request):
    # Obtenez l'étudiant connecté
    etudiant = get_object_or_404(CustomUser, id=request.user.id)
    
    # Vérifiez que l'utilisateur est bien un étudiant
    if etudiant.user.is_etudiant:  # Assurez-vous que cet attribut existe
        # Récupérez tous les résultats associés à l'étudiant
        resultats = Resultat.objects.filter(etudiant=etudiant)

        return render(request, 'Resultat.html', {'etudiant': etudiant, 'resultats': resultats})
    else:
        # Si l'utilisateur n'est pas un étudiant, redirigez ou affichez un message d'erreur
        return render(request, 'error.html', {'message': "Accès non autorisé."})


def envoyé_recours(request, *args, **kwargs):
        # Récupérer l'email de l'administrateur depuis les paramètres de configuration
    admin_email = 'mupendakimpulengegaston@gmail.com'
    
    if request.method == 'POST':
        recours_message = request.POST.get('Recours_message')
        etudiant_email = request.user.email
        # Par exemple, récupérez les détails du recours du formulaire
        sujet = request.POST.get('sujet', 'Recours étudiant')
        message = request.POST.get('message', '')
        email = request.POST.get('email', '')  # S'assurer que l'email est récupéré du formulaire

        # Vérifier que l'email est défini
        if email:
            try:
                send_mail(
                    sujet,
                    message,
                    etudiant_email,  # Utilisateur qui envoie le recours
                    [admin_email],  # Destinataire
                    fail_silently=False,
                )
                messages.success(request, "Votre recours a été envoyé avec succès.")
                return redirect('submit_recours')  
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email: {e}")
        else:
            # Gérer le cas où l'email n'est pas fourni
            return render(request, 'Etudiant/submit_recours.html', {'error': 'L\'adresse e-mail est manquante.'})
    else:
        return render(request, 'Etudiant/submit_recours.html')  # ou récupérer l'email dynamiquement

   
class MatriculeBackend(ModelBackend):
    def authenticate(self, request, matricule=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(matricule=matricule)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

def generate_pdf(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    results = Resultat.objects.filter(Etudiant=etudiant)
    
    template = get_template('bulletin_template.html')
    context = {
        'etudiant': etudiant,
        'results': results,
    }
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="bulletin_{etudiant.nom}.pdf"'

    # Generate the PDF
    HTML(string=html).write_pdf(response)
    
    return response


def submit_recours(request):
      if request.method == 'POST':
        recours_message = request.POST.get('recours_message')
        etudiant_email = request.user.email
        
        # Contenu du message à envoyer
        sujet = "Recours d'un étudiant"
        message = f"Recours envoyé par: {etudiant_email}\nDate: {timezone.now()}\n\nMessage:\n{recours_message}"
        admin_email = settings.ADMIN_EMAIL  # Utilisation du paramètre ADMIN_EMAIL
        
        # Envoyer l'email à l'administrateur
        send_mail(
            sujet,
            message,
            etudiant_email,
            [admin_email],
            fail_silently=False,
        )
        
        # Ajouter un message de confirmation
        messages.success(request, "Votre recours a été envoyé avec succès.")
        return redirect('submit_recours')  # Redirige l'étudiant vers la même page après l'envoi

    # Afficher la page de soumission du recours
      return render(request, 'Etudiant/submit_recours.html', {'date': timezone.now()})


# Fin  Activité Etudiant




# Debut Activité de l'enregistrement enseignant
def register_Enseignant(request):
    if request.method == 'POST':
        enseignant_form = EnseignantRegistrationForm(request.POST, request.FILES)
        if enseignant_form.is_valid():
            try:
                email = enseignant_form.cleaned_data['email']
                if CustomUser.objects.filter(email=email).exists():
                    enseignant_form.add_error('email', 'L\'adresse e-mail saisie existe déjà.')
                else:
                    # Créez l'utilisateur CustomUser
                    user = CustomUser.objects.create_user(
                        email=email,
                        password=enseignant_form.cleaned_data['motdepasse'],
                        nom=enseignant_form.cleaned_data['nom'],
                        postnom=enseignant_form.cleaned_data['postnom'],
                        prénom=enseignant_form.cleaned_data['prénom'],
                        adressephysique=enseignant_form.cleaned_data['adressephysique'],
                        telephone=enseignant_form.cleaned_data['telephone'],
                        user_type='enseignant',  # Assurez-vous que c'est enseignant
                    )

                    # Définir le type d'utilisateur
                    user.user_type = 'enseignant'
                    user.save()

                    # Créez l'objet Enseignant associé
                    enseignant = enseignant_form.save(commit=False)
                    enseignant.user = user
                    enseignant.numero_employe = generate_numero_employe()  # Générer le numero_employe
                    enseignant.profile_picture = enseignant_form.cleaned_data.get('profile_picture')
                    enseignant.save()

                    messages.success(request, "Enseignant enregistré avec succès. En attente de validation.")

                    # Connectez l'utilisateur après l'enregistrement
                    login(request, user)
                    return redirect('Enseignant/TBD_Enseignant')

            except IntegrityError as e:
                enseignant_form.add_error(None, f'Erreur lors de la création du compte: {e}')
    else:
        enseignant_form = EnseignantRegistrationForm()

    return render(request, 'deroulement/register_enseignant.html', {'form': enseignant_form})

def login_Enseignant(request):
    if request.method == 'POST':
        form = EnseignantLoginForm(data=request.POST)
        if form.is_valid():
            numero_employe = form.cleaned_data.get('nom')  # Récupère le matricule saisi
            motdepasse = form.cleaned_data.get('password')  # Récupère le mot de passe saisi 
            user = authenticate(request, username=numero_employe, password=motdepasse)

            if user is not None and user.is_Enseignant:
                login(request, user)
                return redirect('TBD_Enseignant')
        else:
             form.add_error(None, "numéro ou mot de passe incorrect.")
        # Si l'utilisateur n'est pas un enseignant, afficher un message d'erreur

    else:
        form = EnseignantLoginForm(data=request.POST)
    return render(request,'Enseignant/login_Enseignant.html')  


def signup_Enseignant(request):
       if request.method == 'POST':
        form = EnseignantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Grille_de_cote')
        else:
            form = EnseignantSignUpForm()
            return render(request, 'signup_Enseignat.html', {'form': form})

def enseignant_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.user.is_Enseignant))
    return decorated_view_func(view_func)

def TBD_Enseignant(request):
    return render(request, 'Enseignant/TBD_Enseignant.html')

def Grille_de_cote(request):
    if request.method == 'POST':
        form = Grille_de_coteForm(request.POST)
        if form.is_valid():
            resultat = form.save(commit=False)
            
            # Calcul automatique du total
            resultat.total = (
                form.cleaned_data['travail_pratique'] +
                form.cleaned_data['interrogation'] +
                form.cleaned_data['examen']
            )
            
            # Calcul de la moyenne et pourcentage
            resultat.moyenne = resultat.total / 3
            resultat.pourcentage = (resultat.moyenne / 20) * 100
            
            # Détermination de la mention
            resultat.mention = determine_mention(resultat.pourcentage)

            # Message de confirmation
            confirm = request.POST.get('confirm', False)
            if not confirm:
                messages.info(request, "Êtes-vous sûr de vouloir valider ce résultat pour l'étudiant matricule: {}?".format(resultat.etudiant.matricule))
                return render(request, 'Enseignant/Grille_de_cote.html', {'form': form, 'resultats': Resultat.objects.all(), 'confirmation': True})

            resultat.save()
            messages.success(request, "Notes enregistrées avec succès!")
            return redirect('TBD_Enseignant')
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = Grille_de_coteForm()
    
    resultats = Resultat.objects.all()
    return render(request, 'Enseignant/Grille_de_cote.html', {'form': form, 'resultats': resultats})



def determine_mention(self):
        if self.credits_capitalises >= 60:
            return 'Admis'
        elif self.credits_capitalises >= 60 and cote >= 8/20 :
            return 'Acompte'
        elif self. credits_capitalises>= 45:
            return 'Defayant'
        else:
            return 'Ajournée'


def saisie_notes(request):
    if request.method == 'POST':
        form = ResultatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('TBD_Enseignant')  # Replace 'resultat_list' with your desired redirect URL
    else:
        form = ResultatForm()

    return render(request, 'Enseignant/saisie_notes.html', {'form': form})
    
def cote_etudiants_enregistrer(request):
    if request.method == 'POST':
        form = Grille_de_coteForm(request.POST)
        if form.is_valid():
            # Save form but don't commit to the database yet
            resultat = form.save(commit=False)
            
            # Access the cleaned data for the calculated fields
            resultat.total = form.cleaned_data['total']
            resultat.moyenne = form.cleaned_data['moyenne']
            resultat.pourcentage = form.cleaned_data['pourcentage']
            
            # Save the object to the database
            resultat.save()

            messages.success(request, "Notes enregistrées avec succès!")
            return redirect('TBD_Enseignant')  # Adjust the URL name as needed
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = Grille_de_coteForm()

    return render(request, 'Enseignant/cote_enregistrer.html', {'form': form})

@login_required
def fichedecotation(request):
    if request.method == 'POST':
        form = ResultatForm(request.POST)
        if form.is_valid():
             form.save()
        return redirect('Enseignant/fihedecotation')  # Create a success page or redirect to a relevant page
            
    else:
        form = ResultatForm()
    return render(request, 'Enseignant/Grille_de_cote.html', {'form': form})

@receiver(pre_save, sender=Enseignant)
def assign_numero_employe(sender, instance, **kwargs):
    if not instance.numero_employe:
        instance.numero_employe = generate_numero_employe()

    # Fin  Activité Enseignant


# debut  Activité Admin
def is_admin(user):
    return user.groups.filter(name='Administrateur').exists()  

@receiver(post_save, sender=User)
def notify_admin_new_user(sender, instance, created, **kwargs):
    if created:
        subject = 'Nouveau utilisateur créé'
        message = f'Un nouvel utilisateur a été créé : {instance.nom}'
        from_email = 'mupendakimpulengegaston@gmail.com'
        recipient_list = ['mupendakimpulengegaston@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
@staff_member_required
def validate_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin')  # Redirige vers le tableau de bord de l'administrateur

def send_validation_message(sender, request, user, **kwargs):
    if user.first_login:
        # Send validation message
        send_mail(
            'Bien venue sur votre portail',
            'Votre compte est crée et enregistrer avec succe.',
            'mupendakimpulengegaston@gmail.com',
            [user.email],
            fail_silently=False,
        )
        user.first_login = False
        user.save()

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'date_joined')
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = CustomUser.objects.count()
        return super(UserAdmin, self).changelist_view(request, extra_context=extra_context)
 

def utilisateur(request):
    return render(request, 'IscApp/utilisateur.html')

def create_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.numero_employe = generate_numero_employe()  # Génération automatique
            utilisateur.save()
            return redirect('success')  # Redirige vers une page de succès après la sauvegarde
    else:
        form = UtilisateurForm()
    return render(request, 'create_utilisateur.html', {'form': form})

def generate_numero_employe(order_number):
    last_employe = Enseignant.objects.order_by('-id').first()
    new_number = 'ISC' + str(1000 + (last_employe.id if last_employe else 0) + 1)
    return 'ISC' + str(CustomUser.objects.count() + 1).zfill(4)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'IscApp/profile.html', {'form': form})

def user_auth(request):
    return render(request, 'IscApp/user_auth.html')

def Resultat(request):
    utilisateur = request.user
    
    # Vérifiez que l'utilisateur est un étudiant
    if utilisateur.user_type != 'etudiant':
        # Rediriger ou afficher un message d'erreur
        return render(request, 'includes/Erreur.html', {'message': "Vous n'avez pas accès à cette page."})
    
    # Récupérer tous les résultats associés à cet utilisateur
    resultats = Resultat.objects.filter(etudiant=utilisateur).order_by('-date_ajout')
    
    # Calculer les totaux pour les crédits, moyenne annuelle, etc.
    total_credits = sum(resultat.credits for resultat in resultats)
    credits_valides = sum(resultat.credits for resultat in resultats if resultat.pourcentage >= 50)
    credits_non_valides = total_credits - credits_valides
    moyenne_annuelle = sum(resultat.moyenne for resultat in resultats) / resultats.count() if resultats.exists() else 0
    total_travail_pratique = sum(resultat.travail_pratique for resultat in resultats)
    total_UE = sum(resultat.total for resultat in resultats)

    # Vérifier si l'administrateur a autorisé la publication des résultats
    # Vous devez avoir un champ dans le modèle Resultat ou une autre table pour stocker cette information
    autorise_par_admin = utilisateur.etudiant.est_autorise  # Supposons que ce champ existe dans le modèle Etudiant
    
    if not autorise_par_admin:
        return render(request, 'includes/Erreur.html', {'message': "Vos résultats ne sont pas encore publiés."})

    context = {
        'results': resultats,
        'total_credits': total_credits,
        'credits_valides': credits_valides,
        'credits_non_valides': credits_non_valides,
        'moyenne_annuelle': moyenne_annuelle,
        'total_travail_pratique': total_travail_pratique,
        'total_cours': total_cours,
        'annee_academique': timezone.now().year,  # Année académique en cours
        'promotion': utilisateur.promotion,  # La promotion de l'étudiant
        'session_status': 'fermée'  # Indiquer si la session est fermée ou ouverte
    }

    return render(request, 'Etudiant/Resultat.html', context)


    

def archives(request):
    return render(request,'Etudiant/archives.html')
        
        
def fichedecotation(request):
    if request.method == 'POST':
        form = ResultatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Enseignant/fihedecotation')  # Redirigez après avoir enregistré le formulaire
    else:
        form = ResultatForm()  # Enlevez les parenthèses supplémentaires ici

    resultats = Resultat.objects.filter(etudiant=request.user)
    current_year = datetime.now().year  # Récupérer l'année actuelle
    return render(request, 'Resultat.html', {'results': resultats, 'current_year': current_year})

@login_required
def valider_resultats(request):
    if request.user.is_superuser:
        # Logique pour valider les résultats
        pass
    else:
        messages.error(request, "Vous n'êtes pas autorisé à voir cette page.")
        return redirect('home')

@login_required
def resultat_view(request):
    user = request.user
    if user.user_type == 'etudiant':
        resultats = Resultat.objects.filter(etudiant=user)
        return render(request, 'Etudiant/Resultat.html', {'resultats': resultats})
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')

@staff_member_required
def valider_notes(request):
    # Récupérer toutes les notes en attente de validation
    notes_a_valider = Resultat.objects.filter(est_valide=False)
    
    if request.method == 'POST':
        # Parcourir les notes et les marquer comme validées
        for resultat in notes_a_valider:
            resultat.est_valide = True
            resultat.save()
        return redirect('admin_dashboard')  # Redirigez après validation

    return render(request, 'ValiderNotes.html', {'notes_a_valider': notes_a_valider})


class numero_employeBackend(ModelBackend):
    def authenticate(self, request, numero_employe=None, password=None, **kwargs):
        try:
            Enseignant = Enseignant.objects.get(numero_employe=numero_employe)
            if Enseignant.check_password(password):
                return Enseignant
        except Enseignant.DoesNotExist:
            return None

def logout_view(request):
    logout(request)
    return redirect('login')

def generate_matricule(sexe, order_number):
    # I + order number + gender initial + current year + order number again + G
    current_year = datetime.now().year
    gender_initial = 'M' if sexe == 'M' else 'F'
    matricule = f"I{order_number}{gender_initial}C0{current_year % 100}{order_number}G"
    return matricule

def create_etudiant(request):
    if request.method == 'POST':
        form = etudiant_form(request.POST)
        if etudiant_form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.matricule = generate_matricule(etudiant.sexe)  # Génération automatique
            etudiant.save()
            return redirect('home')  # Redirige vers une page de succès après la sauvegarde
    else:
        form = EtudiantForm()
    return render(request, 'register_etudiant.html', {'form': form})

def soumettre_Deliberation(request):
    return render(request,'soumettre_Deliberation.html')

# fin premier activite admin

# bouton recheche
def search(request):
    query = request.GET.get('q')
    results = []  # Logic to get results based on the query
    # Filter out results like passwords, matricules, etc.
    # results = YourModel.objects.filter(...).exclude(...)
    return render(request, 'IscApp/search_results.html', {'results': results})

def search_results(request):
    form = SearchForm(request.GET)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']

        # Search across multiple models and fields
        etudiant_results = Etudiant.objects.filter(
            Q(nom__icontains=query) |
            Q(postnom__icontains=query) |
            Q(prénom__icontains=query) |
            Q(option_section__icontains=query)
        ).exclude(matricule__icontains=query)

        enseignant_results = Enseignant.objects.filter(
            Q(nom__icontains=query) |
            Q(postnom__icontains=query) |
            Q(prénom__icontains=query) |
            Q(specialite__icontains=query) |
            Q(UE__icontains=query)
        ).exclude(numero_employe__icontains=query).exclude(motdepasse__icontains=query)

        ue_results = ue.objects.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(code__icontains=query)
        )

        # Combine the results
        results = list(etudiant_results) + list(enseignant_results) + list(ue_results)

    return render(request, 'search_results.html', {'form': form, 'results': results})

# photo de profil
@login_required
def profile(request):
    if profile_id:
        # Modification existante
        profile = get_object_or_404(Profile, id=profile_id)
    else:
        # Nouveau profil
        profile = Profile()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil enregistré avec succès.")
            return redirect('profile_list')  # Redirection vers une page de liste de profils ou une autre page de votre choix
        else:
            messages.error(request, "Erreur lors de l'enregistrement du profil. Veuillez vérifier les champs.")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'IscApp/profile.html', {'form': form})

    

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'Etudiant'):
            return '/TableauDeBord/'  # Redirect for students
        elif hasattr(user, 'Enseignant'):
            return '/TBD_Enseignant/'  # Redirect for teachers
        return super().get_success_url()

@login_required
def profile_edit(request, profile_id=None):
    if profile_id:
        # Modification existante
        profile = get_object_or_404(Profile, id=profile_id)
    else:
        # Nouveau profil
        profile = Profile()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil enregistré avec succès.")
            return redirect('profile_list')  # Redirection vers une page de liste de profils ou une autre page de votre choix
        else:
            messages.error(request, "Erreur lors de l'enregistrement du profil. Veuillez vérifier les champs.")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'IscApp/profile.html', {'form': form})


# Etats de sortie qu'on peut imprimer
    
def imprimer_pdf(request, pk):
    objet = resultat.objects.get(pk=pk)
    html_string = render_to_string('imprimer_pdf.html', {'objet': objet})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{objet.nom}.pdf"'
    html.write_pdf(response)
    return response

class Command(BaseCommand):
    help = 'Importe les promotions depuis un fichier CSV'

    def handle(self, *args, **kwargs):
        with open('promotions.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Promotion.objects.create(nom=row['nom'], description=row['description'])
        self.stdout.write(self.style.SUCCESS('Importation des promotions terminée.'))

def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'impression/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

def imprimir_pdf(request):
    # Fetch the data
    promotions_concerned = Promotion.objects.filter(declared=True)
    promotions_not_deliberated = Promotion.objects.filter(declared=False)
    
    # Create a PDF response
    template_path = 'pdf_template.html'
    context = {
        'promotions_concerned': promotions_concerned,
        'promotions_not_deliberated': promotions_not_deliberated,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="promotions.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def promotion(request):
    promotions_concerned = promotion.objects.filter(declared=True)
    promotions_not_deliberated = promotion.objects.filter(declared=False)
    probable_dates = {
        promo: Deliberation.objects.filter(promotion=promo).first().probable_date
        for promo in promotions_not_deliberated
    }

    context = {
        'promotions_concerned': promotions_concerned,
        'promotions_not_deliberated': promotions_not_deliberated,
        'probable_dates': probable_dates,
    }
    return render(request, 'impression/information.html', context)

def Liste_Deliberation(request):
    return render(request, 'liste_Deliberation.html')

# Fin des etats de sotie


# envoie de mail pour le parties

def envoyer_email(sujet, message, destinataires):
    send_mail(
        sujet,
        message,
        settings.EMAIL_HOST_USER,  # Expéditeur
        destinataires,  # Liste des destinataires
        fail_silently=False,
    )

def creer_objet(request):
    if request.method == 'POST':
        # Traitement de la création d'objet
        objet = VotreModele.objects.create(...)
        # Envoyer un e-mail après la création
        envoyer_email(
            'Objet Créé',
            f'L\'objet {objet.nom} a été créé avec succès!',
            ['destinataire@gmail.com']
        )
        return redirect('liste_objets')
    return render(request, 'creer_objet.html')

# NOTIFICATION
def notifications(request):
    return render (request,'notification.html')

# Radio Okapi

def radio_okapi_feed(request):
    feed_url ='https://www.radiookapi.net/content/fil-rss'
    feed = feedparser.parse(feed_url)
    entries = feed.entries[:5]  # Limitez à 5 articles, vous pouvez ajuster ce nombre

    context = {
        'feed_entries': entries,
    }
     # Debugging
    print(f"Number of entries fetched: {len(entries)}")
    for entry in entries:
        print(f"Title: {entry.title}")

    context = {
        'feed_entries': entries,
    }

    return render(request, 'IscApp/Radio_okapi.html', context)

    
def listepromotion(request):
    promotions = Promotion.objects.all()  # Récupérez toutes les promotions
    print(promotions)  # Affichez dans la console pour vérifier
    # Passez les promotions à votre template ou effectuez une autre opération
    return render(request, 'listepromotion.html', {'promotions': promotions})

# etat de sortie proprement dit


def informations_promotions(request):
    # Obtenez les promotions concernées par la délibération
    promotions_concerned = Promotion.objects.filter(is_deliberated=True)

    # Obtenez les promotions non délibérées
    promotions_not_deliberated = Promotion.objects.filter(is_deliberated=False)

    # Créez un dictionnaire pour les dates probables de délibération (ceci est juste un exemple)
    probable_dates = {
        promotion.nom: promotion.probable_date for promotion in promotions_not_deliberated
    }

    # Passez les données au template
    context = {
        'promotions_concerned': promotions_concerned,
        'promotions_not_deliberated': promotions_not_deliberated,
        'probable_dates': probable_dates
    }
    return render(request, 'impression/informations_promotions.html', context)

@login_required
def submit_grades(request, ue_id):
    # Logic for submitting grades
    UE = get_object_or_404(UE, id=ue_id)
    etudiant = Etudiant.objects.filter(UE=UE)
    
    # After the grades are submitted successfully, create notifications
    for Etudiant in etudiant:
        Notification.objects.create(
            recipient=etudiant.user, 
            message=f"Les résultats pour le cours {ue.nom} sont maintenant disponibles."
        )

    return redirect('home')  # Replace with your desired redirect

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notification.html', {'notifications': notifications})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Peut être matricule ou numero_employe
        password = request.POST.get('password')
        user = authenticate(request, matricule=username, password=password) or authenticate(request, numero_employe=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirige vers le tableau de bord de l'administrateur
            elif user.user_type == 'enseignant':
                return redirect('TBD_Enseignant')  # Redirige vers le tableau de bord de l'enseignant
            elif user.user_type == 'etudiant':
                return redirect('TableauDeBord')  # Redirige vers le tableau de bord de l'étudiant
        else:
            # Erreur d'authentification
            return render(request, 'erreur.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    return render(request, 'home.html')
def admin_dashboard(request):
    # Filtrer les objets nouvellement créés (à adapter selon votre logique)
    nouveaux_etudiants = Etudiant.objects.filter(est_nouveau=True)
    nouveaux_enseignants = Enseignant.objects.filter(est_nouveau=True)
    nouveaux_cours = Cours.objects.filter(est_nouveau=True)
    nouveaux_resultats = Resultat.objects.filter(est_nouveau=True)

    context = {
        'nouveaux_etudiants': nouveaux_etudiants,
        'nouveaux_enseignants': nouveaux_enseignants,
        'nouveaux_cours': nouveaux_cours,
        'nouveaux_resultats': nouveaux_resultats,
    }

    return render(request, 'admin/dashboard.html', context)



