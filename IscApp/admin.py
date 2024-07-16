from django.contrib import admin
from . models import utilisateur, Etudiant, Enseignant, cours, inscription, note, Resultat,CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    ('Enseigant', 'Etudiant')

# Register your models here.
@admin.register(utilisateur)
class utilisateurAdmin(admin.ModelAdmin):
    list_display = ('id','nom','postnom', 'prénom','telephone', 'email')

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('id','nom', 'postnom','prénom', 'email','telephone', 'matricule','motdepasse')

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'postnom', 'prénom', 'email', 'numero_employe')

@admin.register(cours)
class coursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'code', 'Enseignant')

@admin.register(inscription)
class inscriptionAdmin(admin.ModelAdmin):
    list_display = ('date_inscription', 'etudiant', 'cours')

@admin.register(note)
class noteAdmin(admin.ModelAdmin):
    list_display = ('valeur', 'date_attribution', 'etudiant', 'cours')

@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('moyenne', 'mention', 'etudiant', 'cours')


