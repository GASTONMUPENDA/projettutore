from django.contrib import admin
from . models import CustomUser, Etudiant, Enseignant, Resultat,CustomUser,Promotion,UE


class CustomUserAdmin(admin.ModelAdmin):
    ('Enseigant', 'Etudiant','admin')

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','nom','postnom', 'prénom','adressephysique','email','telephone','motdepasse' )

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'option_section', 'sexe','lieu_naissance','date_naissance','nationalite','profile_picture')

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('id','numero_employe','specialite','Promotion','option_section','profile_picture')

@admin.register(UE)
class UEAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'code','enseignant')


@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'ue','semestre','matiere','categorie','credit','cote','credits_capitalises','notes','travail_pratique','interrogation','examen','total','moyenne','pourcentage','validation','mention','date_ajout','is_authorized')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'is_deliberated', 'probable_date')
    search_fields = ('nom',)
    list_filter = ('is_deliberated', 'probable_date')


