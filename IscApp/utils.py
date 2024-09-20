import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Enseignant

logger = logging.getLogger(__name__)

def send_email_with_html_body(subject: str, receivers: list, template: str, context: dict):
    """Cette fonction aide à envoyer le mail"""
    try:
        message = render_to_string(template, context)

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            receivers,
            fail_silently=True,
            html_message=message
        )

        return True

    except Exception as e:
        logger.error(e)

    return False

def generate_numero_employe():
    """Génère un numéro d'employé unique"""
    # Obtenez le dernier numéro d'employé créé
    last_enseignant = Enseignant.objects.order_by('numero_employe').last()

    if not last_enseignant:
        # Commencez par 'ISC001' si aucun enseignant n'existe encore
        return 'ISC001'

    # Extraire le numéro de la partie du dernier numero_employe
    last_number = int(last_enseignant.numero_employe.split('ISC')[-1])
    new_number = last_number + 1

    # Retourne le nouveau numéro d'employé formaté
    return f'ISC{new_number:03d}'
