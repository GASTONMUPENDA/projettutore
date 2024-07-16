from django.shortcuts import render, redirect
from django.contrib.auth import login , authenticate, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .forms import EtudiantCreationForm, EtudiantLoginForm, CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EtudiantCreationForm, EtudiantLoginForm
from django.http import HttpResponseRedirect


def home(request):
    return render(request, 'IscApp/home.html')

def cours(request):
    return render(request, 'IscApp/cours.html')

def user_choice(request):
   
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'Etudiant':
            return redirect(reverse( 'IscApp/register_Etudiant'))
        elif user_type == 'Enseignant':
            return redirect(reverse_lazy('IscApp/register_Enseignant'))
    return render(request, 'IscApp/user_choice.html')

class SignupView(CreateView):
    form_class = CustomUser
    template_name = 'IscApp/signup.html'
    success_url = reverse_lazy('login_Etudiant')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'IscApp/login.html'

def register_Etudiant(request):
    if request.method == 'POST':
        form = EtudiantCreationForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            return redirect('TableauDeBord')
    else:
        form = EtudiantCreationForm()
    return render(request, 'IscApp/register_Etudiant.html',{'form':form})


def login_Etudiant(request):
    if request.method == 'POST':
        form = EtudiantLoginForm(request, data=request.POST)
        if form.is_valid():
            matricule = form.cleaned_data.get('matricule')
            motdepasse = form.cleaned_data.get('motdepasse')
            utilisateur = authenticate(matricule=matricule, motdepasse=motdepasse)
            utilisateur = authenticate(nom=form.cleaned_data.get('matricule'), motdepasse = form.cleaned_data.get('motdepasse'))
            if utilisateur is not None:
                login(request, utilisateur)
                return redirect('TableauDeBord')

    else:
        form = EtudiantLoginForm()
    return render(request, 'IscApp/login_etudiant.html',{'form':form})  

@login_required
def TableauDeBord(request):
    return(request,'IscApp/TableauDeBord.html')

class CustomLoginView(LoginView):
    template_name = 'login_Etudiant.html'
    success_url = reverse_lazy('TableauDeBord')

class registerEtudiantView(CreateView):
    form_class =  EtudiantCreationForm
    template_name = 'register_Etudiant.html'
    success_url = reverse_lazy('login_Etudiant')





def Enseignant(request):
    return render(request, 'IscApp/Enseignant.html')



def search_results(request):
    return render(request, 'IscApp/search_results.html')

def notifications(request):
    return render(request, 'IscApp/notifications.html')

def utilisateur(request):
    return render(request, 'IscApp/utilisateur.html')

def profile(request):
    return render(request, 'IscApp/profile.html')


def user_auth(request):
    return render(request, 'IscApp/user_auth.html')
