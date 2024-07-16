from django.utils.deprecation import MiddlewareMixin


class ClickjackingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if hasattr(response, 'get') and callable(response.get):
            if response.get("X-Frame-Options") is not None:
              return response
        # Ajoutez d'autres manipulations de la réponse si nécessaire
        return response