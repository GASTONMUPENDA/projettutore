from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission,BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=50)
    postnom = models.CharField(max_length=50)
    prénom = models.CharField(max_length=50)
    adressephysique = models.CharField(max_length=560, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    motdepasse = models.CharField(max_length=50, default='default_motdepasse')

     # Champs supplémentaires
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    USER_TYPE = (
        ('administrateur', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Etudiant'),
    )

    user_type = models.CharField(max_length=15, choices=USER_TYPE, default='etudiant')
    # Champs requis pour le système d'authentification Django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # Custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'postnom', 'prénom']

    def save(self, *args, **kwargs):
        if self.is_superuser:
           self.user_type = 'administrateur'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - {self.nom} {self.postnom}"

    def is_etudiant(self):
        return self.user_type == 'etudiant'

    def is_enseignant(self):
        return self.user_type == 'enseignant'

    def is_administrateur(self):
        return self.user_type == 'administrateur'

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
   

class Etudiant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='etudiant_profile')
    matricule = models. CharField(max_length=50, unique=True)
    Promotion =  models.ForeignKey('Promotion', on_delete=models.CASCADE, related_name='etudiants', blank=True, null=True)
    option_section = models.CharField(max_length=100, default='default_section')
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    lieu_naissance = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    nationalite = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    def __str__(self):
        return f"{self.matricule}"


class Enseignant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enseignant_profile')
    numero_employe = models. CharField(max_length=50, unique=True)
    specialite = models.CharField(max_length=100)
    Promotion =  models.ForeignKey('Promotion', on_delete=models.CASCADE, related_name='enseignants', blank=True, null=True)
    option_section = models.CharField(max_length=100, default='default_section')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) 

    def __str__(self):
        return f"{self.numero_employe}"




class UE(models.Model):
    nom = models.CharField(max_length=100,default=5)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    enseignant = models.ForeignKey('Enseignant', on_delete=models.CASCADE, related_name='ue')
    

    def __str__(self):
        return self.nom



class Resultat(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='resultats')
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='resultats',default="ue")
    semestre = models.CharField(
        max_length=20,
        choices=[('Premier Semestre', 'Premier Semestre'), ('Deuxième Semestre', 'Deuxième Semestre')],
        default='semestre'
    )
    matiere = models.CharField(max_length=100, blank=True)  # MATIERES (E.C)
    categorie = models.CharField(
        max_length=2,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C')],
        blank=True
    )  # CATEGORIE field
    credit = models.IntegerField(default=0)  # CREDIT field
    cote = models.FloatField(default=0.0)  # COTE /20 field
    credits_capitalises = models.IntegerField(default=0)  # CREDITS CAPITALISES field
    notes = models.TextField(blank=True)  # NOTES field
    travail_pratique = models.FloatField(default=0.0)
    interrogation = models.FloatField(default=0.0)
    examen = models.FloatField(default=0.0)
    total = models.FloatField(blank=True, default=0.0)
    moyenne = models.FloatField(blank=True, default=0.0)
    pourcentage = models.FloatField(blank=True, default=0.0)
    validation = models.CharField(
        max_length=20,
        choices=[('Validé', 'Validé'), ('Non validé', 'Non validé')],
        blank=True
    )  # VALIDATION field
    mention = models.CharField(max_length=20, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    is_authorized = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'ue')

    def save(self, *args, **kwargs):
        self.total = self.travail_pratique + self.interrogation + self.examen
        self.moyenne = self.total / 20
        self.pourcentage = self.moyenne * 5
        self.mention = self.assign_mention()
        super().save(*args, **kwargs)

    def assign_mention(self):
        if self.credits_capitalises >= 60:
            return 'Admis'
        elif self.credits_capitalises >= 60 and cote >= 8/20 :
            return 'Acompte'
        elif self. credits_capitalises>= 45:
            return 'Defayant'
        else:
            return 'Ajournée'

    def __str__(self):
        return f"Résultat de {self.etudiant.matricule} pour le cours {self.cours}"



class Promotion(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(default=True)
    is_deliberated = models.BooleanField(default=False)
    probable_date = models.DateField(null=True, blank=True)  # Utilisez DateField pour les dates simples 
    
    def __str__(self):
        return f'{self.nom}'

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)





