from django.http import JsonResponse
from functools import wraps

from video_server.settings import AUTH_STATIC_TOKEN


def authenticate_api(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token != f"Bearer {AUTH_STATIC_TOKEN}":
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return func(request, *args, **kwargs)

    return wrapper
