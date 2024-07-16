from django.contrib import admin
from django.urls import path
from IscApp.views import home, cours, EtudiantCreationForm, Enseignant, search_results, notifications, utilisateur, profile, SignupView, CustomLoginView, register_Etudiant, user_choice, user_auth, login_Etudiant,TableauDeBord

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cours/', cours, name='cours'),
    path('EtudiantCreationForm/', EtudiantCreationForm, name='EtudiantCreationForm'),
    path('Enseignant/', Enseignant, name='Enseignant'),
    path('search_results/', search_results, name='search_results'),
    path('notifications/', notifications, name='notifications'),
    path('utilisateur/', utilisateur, name='utilisateur'),
    path('profile/', profile, name='profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register_Etudiant/', register_Etudiant, name='register_Etudiant'),
    path('user_choice/', user_choice, name='user_choice'),
    path('register_Etudiant/', register_Etudiant, name='register_Etudiant'),
    path('login_Etudiant/', login_Etudiant, name='login_Etudiant'),
    path('TableauDeBord/', TableauDeBord, name='TableauDeBord'),
] 
