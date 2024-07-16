from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE = (
        (1,'Enseignant'),
        (2,'Etudiant'),
    )
    user_type = models.IntegerField(choices=USER_TYPE, default=2)

    email =models.EmailField(unique=True)
    is_Enseignat = models.BooleanField(default=False)
    is_Etudiant = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
    
    groups = models.ManyToManyField(
        
        Group,
        related_name= 'CustomUser_set',
        blank = True,
        help_text = 'the groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name = 'groups'
        )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='Custom_User_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    

class utilisateur(models.Model):
    
       
    
    nom = models.CharField(max_length =50)
    postnom = models.CharField(max_length =50)
    prénom = models.CharField(max_length =50)
    adressephysique = models.CharField(max_length =560,null=True, blank=True)
    email = models.CharField(max_length =200)
    telephone = models.CharField(max_length =50,null=True, blank=True)
    motdepasse = models.CharField(max_length =50)
    
    def  __str__(self):
       return self.matricule
    
class Etudiant(utilisateur):
    user = models.OneToOneField('CustomUser',on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, unique=True)
    image=models.ImageField()
    sexe=models.TextField()
    lieunaissance=models.TextField()
    date_naissance=models.DateField(null=True, blank=True)
    nationalité=models.TextField()

    
    def  __str__(self):
       return "{self.matricule } {self.nom} {self.postnom} {self.prénom}"


Etudiant.objects.all()
Etudiant.objects.filter(matricule__contains="nom")
Etudiant.objects.filter(matricule__icontains="nom")

class Enseignant(utilisateur):
      user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
      numero_employe = models.CharField(max_length=20, unique=True)
      specialite = models.CharField(max_length=100)

class cours(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    Enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, default =1)

    
    def  __str__(self):
       return self.matricule

class inscription(models.Model):
    date_inscription = models.DateField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(cours, on_delete=models.CASCADE)

    
    def  __str__(self):
       return self.matricule

class note(models.Model):
    valeur = models.FloatField()
    date_attribution = models.DateField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(cours, on_delete=models.CASCADE)
    
    def  __str__(self):
       return self.matricule

class Resultat(models.Model):
    moyenne = models.FloatField()
    mention = models.CharField(max_length=20)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(cours, on_delete=models.CASCADE)
    
    def  __str__(self):
       return self.matricule

class profil(models.Model):

    
    def __str__(self):
        return self.usename


    