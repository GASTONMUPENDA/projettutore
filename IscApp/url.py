from django.contrib import admin
from django.urls import path
from IscApp.views import home, navebare,UE, EtudiantCreationForm, Enseignant, register_Enseignant,login_Enseignant,search_results, notifications, CustomUser, profile,delete_profile_picture, SignupView, CustomLoginView, register_Etudiant, user_choice, user_auth, login_Etudiant,TableauDeBord,TBD_Enseignant,signup_Enseignant,Saisir_notes,Liste_Deliberation,soumettre_Deliberation,radio_okapi_feed,Resultat,MatriculeBackend,voir_resultats,generate_pdf,, imprimer_pdf,submit_recours,promotion,login,Grille_de_cote,fichedecotation,listepromotion,informations_promotions,saisie_notes, cote_etudiants_enregistrer,archives
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('navbare/',navbare, name='navebare'),
    path('UE/', UE, name='UE'),
    path('EtudiantCreationForm/', EtudiantCreationForm, name='EtudiantCreationForm'),
    path('Enseignant/', Enseignant, name='Enseignant'),
    path('search_results/', search_results, name='search_results'),
    path('notifications/', notifications, name='notifications'),
    path('CustomUser/', CustomUser, name='CustomUser'),
    path('profile/', profile, name='profile'),
    path('profile/delete/', views.delete_profile_picture, name='delete_profile_picture'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', login, name='login'),
    path('register_Etudiant/deroulement/TableauDeBord', register_Etudiant, name='TableauDeBord'),
    path('user_choice/', user_choice, name='user_choice'),
    path('register_Enseignant/', register_Enseignant, name='register_Enseignant'),
    path('login_Etudiant/', login_Etudiant, name='login_Etudiant'),
    path('TableauDeBord/', TableauDeBord, name='TableauDeBord'),
    path('login_Enseignant/', login_Enseignant, name='login_Enseignant'),
    path('Resultat/', Resultat, name='Resultat'),
    path('archives/',archives, name = archives),
    path('signup_Enseignant/',signup_Enseignant, name='signup_Enseignant'),
    path('Saisir_notes/', Saisir_notes, name='Saisir_notes'),
    path('Liste_Deliberation/',Liste_Deliberation, name='Liste_Deliberation'),
    path('soumettre_Deliberation/',soumettre_Deliberation, name='soumettre_Deliberation'),
    path('MatriculeBackend/', MatriculeBackend, name='MatriculeBackend'),
    path('radio-okapi-feed/',radio_okapi_feed, name='radio_okapi_feed', name='home'),

    path('fichedecotation/', fichedecotation, name='fichedecotation'),
    path('voir_resultats/', voir_resultats, name='voir_resultats'),
    path('envoyé_recours/', envoyé_recours, name='envoyé_recours'),
    path('TBD_Enseingnant/', TBD_Enseingnant, name= 'TBD_Enseignant'),
    path('generate_pdf/<int:etudiant_id>/', generate_pdf, name='generate_pdf'),
    path('imprimer/<int:pk>/', imprimer_pdf, name='imprimer_pdf'),
    path('submit_recours/', submit_recours, name='submit_recours'),
    path('promotion/', promotion, name='promotion'),
    path('grille_de_cote/',Grille_de_cote, name ='Grille_de_cote'),
    path('listepromotion/',listepromotion, name = 'listepromotion'),
    path('informations_promotions/',informations_promotions, name ='informations_promotions'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('saisie_notes/',saisie_notes,name='saisie_notes'),
    path('cote_etudiants_enregistrer/',cote_etudiants_enregistrer,name ='cote_etudiants_enregistrer'),
    path('determine_mention/',determine_mention,name = 'determine_mention'),
]