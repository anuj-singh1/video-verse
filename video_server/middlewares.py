from django.conf import settings
from django.http import JsonResponse


class RequestAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return JsonResponse({'error': 'Authorization token is required'}, status=401)

        # Verify the token
        static_token = getattr(settings, 'AUTH_STATIC_TOKEN', None)
        if token != f"Bearer {static_token}":
            return JsonResponse({'error': 'Invalid authorization token'}, status=401)

        return self.get_response(request)
