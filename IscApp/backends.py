# IscApp/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Etudiant,Enseignant

class MatriculeBackend(BaseBackend):
    def authenticate(self, request, matricule=None, password=None, **kwargs):
        CustomUser = get_user_model()
        try:
            # Cherchez le champ matricule dans le modèle Etudiant
            etudiant = Etudiant.objects.get(matricule=matricule)
            user = etudiant.user  # Récupère l'utilisateur lié à l'étudiant
            if user.check_password(password) and user.user_type == 'etudiant':
                return user
        except Etudiant.DoesNotExist:
            return None

    def get_user(self, user_id):
        CustomUser = get_user_model()
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

class NumeroEmployeBackend(BaseBackend):
    def authenticate(self, request, numero_employe=None, password=None, **kwargs):
        CustomUser = get_user_model()
        try:
            # Cherchez le champ numero_employe dans le modèle Enseignant
            enseignant = Enseignant.objects.get(numero_employe=numero_employe)
            user = enseignant.user  # Récupère l'utilisateur lié à l'enseignant
            if user.check_password(password) and user.user_type == 'enseignant':
                return user
        except Enseignant.DoesNotExist:
            return None

    def get_user(self, user_id):
        CustomUser = get_user_model()
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
