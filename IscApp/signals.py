# signals.py
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Etudiant, Enseignant, UE, Resultat,CustomUser
from django.utils.crypto import get_random_string

User = get_user_model()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Generate default password
        default_password = get_random_string(length=8)
        instance.set_password(default_password)  # Set default password for the user
        instance.save()

        # Handle teacher profile creation
        if instance.user_type == 'enseignant':
            enseignant_profile = Enseignant.objects.create(user=instance)
            
            # Generate employee number
            employee_number = generate_employee_number()
            enseignant_profile.numero_employe = employee_number
            enseignant_profile.save()
            
            # Send email notification to administrator
            send_admin_notification(instance, 'Enseignant', employee_number, default_password)

        # Handle student profile creation
        elif instance.user_type == 'etudiant':
            etudiant_profile = Etudiant.objects.create(user=instance)
            
            # Generate matricule number
            matricule_number = generate_matricule_number()
            etudiant_profile.matricule = matricule_number
            etudiant_profile.save()
            
            # Send email notification to administrator
            send_admin_notification(instance, 'Etudiant', matricule_number, default_password)

def send_admin_notification(user, user_type, identifier, default_password):
    admin_email = settings.ADMIN_EMAIL  # Set this in your settings.py
    subject = f"Nouveau {user_type} Créé"
    message = (
        f"Un nouvel utilisateur ({user_type}) a été créé.\n\n"
        f"Nom d'utilisateur: {user.username}\n"
        f"Email: {user.email}\n"
        f"Numéro d'identification: {identifier}\n"
        f"Mot de passe par défaut: {default_password}\n\n"
        f"Merci de valider le compte."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])

# signals.py

@receiver(post_save, sender=Etudiant)
def notify_admin_new_etudiant(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Nouveau Étudiant Inscrit',
            f'Un nouvel étudiant a été inscrit : {instance.matricule} {instance.option_section}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

@receiver(post_save, sender=Enseignant)
def notify_admin_new_enseignant(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Nouveau Enseignant Inscrit',
            f'Un nouvel enseignant a été inscrit : {instance.numero_employe} {instance.Promotion}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

@receiver(post_save, sender=UE)
def notify_admin_new_ue(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Nouvelle Unité d enseignement  Ajouté',
            f'Un nouvelle Unité enseignement a été ajouté : {instance.nom}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

@receiver(post_save, sender=Resultat)
def notify_admin_new_resultat(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Nouveau Résultat Publié',
            f'Un nouveau résultat a été publié pour l\'étudiant : {instance.etudiant.nom} {instance.etudiant.postnom} dans unité  : {instance.ue.nom}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

@receiver(post_save, sender=Etudiant)
def assign_matricule(sender, instance, created, **kwargs):
    if created:
        order_number = Etudiant.objects.count()  # Get total count to determine order
        matricule = generate_matricule(instance.sexe, order_number)
        instance.matricule = matricule
        instance.save()

        # Send email notification
        send_mail(
            'Matricule Generated',
            f'Votre matricule est: {matricule}',
            'mupendakimpulengegaston@gmail.com',
            [instance.user.email]
        )

@receiver(post_save, sender=Enseignant)
def assign_numero_employe(sender, instance, created, **kwargs):
    if created:
        order_number = Enseignant.objects.count()  # Get total count to determine order
        numero_employe = generate_numero_employe(order_number)
        instance.numero_employe = numero_employe
        instance.save()

        # Send email notification
        send_mail(
            'Numero Employe Generated',
            f'Votre numero d\'employe est: {numero_employe}',
            'mupendakimpulengegaston@gmail.com',
            [instance.user.email]
        )