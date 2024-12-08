from django.http import JsonResponse
from functools import wraps


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required."}, status=401)
            if request.user.role != required_role:
                return JsonResponse(
                    {"error": f"Permission denied: {required_role} role required."},
                    status=403,
                )
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
