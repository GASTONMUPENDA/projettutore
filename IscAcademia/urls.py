from django.contrib import admin
from django.urls import path
from IscApp.views import home, UE,navbare, EtudiantCreationForm, Enseignant, search_results, notifications, CustomUser, profile, SignupView, CustomLoginView,login, register_Etudiant, user_choice,register_Enseignant, user_auth, login_Etudiant,TableauDeBord,signup_Enseignant,login_Enseignant,Liste_Deliberation,soumettre_Deliberation,radio_okapi_feed,Resultat,MatriculeBackend,numero_employeBackend, TBD_Enseignant,generate_pdf,imprimer_pdf,imprimir_pdf,submit_recours,promotion,Grille_de_cote,fichedecotation,listepromotion,informations_promotions, saisie_notes, cote_etudiants_enregistrer,determine_mention,archives
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('navbare/',navbare, name='navebare'),
    path('deroulement/login/', login, name='login'),
    path('UE/', UE, name='UE'),
    path('EtudiantCreationForm/', EtudiantCreationForm, name='EtudiantCreationForm'),
    path('Enseignant/', Enseignant, name='Enseignant'),
    path('search_results/', search_results, name='search_results'),
    path('notifications/', notifications, name='notifications'),
    path('CustomUser/', CustomUser, name='CustomUser'),
    path('profile/', profile, name='profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register_Enseignant/', register_Enseignant, name='register_Enseignant'),
    path('register_Etudiant/', register_Etudiant, name='register_Etudiant'),
    path('user_choice/', user_choice, name='user_choice'),
    path('login_Etudiant/', login_Etudiant, name='login_Etudiant'),
    path('TableauDeBord/',TableauDeBord, name='TableauDeBord'),
    path('login_Enseignant/', login_Enseignant, name='login_Enseignant'),
    path('signup_Enseignant/',signup_Enseignant, name='signup_Enseignant'),
    path('fichedecotation/', fichedecotation, name='fichedecotation'),
    path('Liste_Deliberation/',Liste_Deliberation, name='Liste_Deliberation'),
    path('soumettre_Deliberation/',soumettre_Deliberation, name='soumettre_Deliberation'),
    path('Resultat/', Resultat, name='Resultat'),
    path('archives/',archives, name ='archives'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('MatriculeBackend/', MatriculeBackend),
    path('numero_employeBackend/',numero_employeBackend),
    path('radio-okapi-feed/',radio_okapi_feed, name=''),
    path('TBD_Enseignant/', TBD_Enseignant, name ='TBD_Enseignant'),
    path('generate_pdf/<int:etudiant_id>/', generate_pdf, name='generate_pdf'),
    path('imprimer/<int:pk>/', imprimer_pdf, name='imprimer_pdf'),
    path('imprimer_pdf/', imprimir_pdf, name='imprimir_pdf'),
    path('submit_recours/', submit_recours, name='submit_recours'),
    path('promotion/',promotion,name='promotion'),
    path('grille_de_cote/',Grille_de_cote, name ='Grille_de_cote'),
    path('listepromotion/',listepromotion, name = 'listepromotion'),
    path('informations_promotions/', informations_promotions, name= 'informations_promotions'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('saisie_notes/', saisie_notes,name ='saisie_notes'),
    path('cote_etudiants_enregistrer/',cote_etudiants_enregistrer,name='cote_etudiants_enregistrer'),
    path('determine_mention/',determine_mention, name ='determine_mention'),
    
] 