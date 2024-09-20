from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import redirect


class ClickjackingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check for the X-Frame-Options header and add it if missing
        if 'X-Frame-Options' not in response:
            response['X-Frame-Options'] = 'DENY'  # Or another value like 'SAMEORIGIN'
        return response

# Dans votre fichier middleware.py

class RedirectBasedOnUserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Votre logique pour la redirection
        user = request.user
        if user.is_authenticated:
            if user.groups.filter(name='Étudiant').exists():
                if request.path != '/TableauDeBord/':
                    return redirect('/TableauDeBord/')
            elif user.groups.filter(name='Enseignant').exists():
                if request.path != '/TBD_Enseignant/':
                    return redirect('/TBD_Enseignant/')
        response = self.get_response(request)
        return response
