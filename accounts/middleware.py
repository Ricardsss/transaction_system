from django.http import JsonResponse


class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        path_role_map = {"/admin-only/": "admin", "/teller-only/": "teller"}

        for restricted_path, required_role in path_role_map.items():
            if (
                request.path.startswith(restricted_path)
                and request.user.role != required_role
            ):
                return JsonResponse(
                    {"error": "Access denied: insufficient permissions."}, status=403
                )
        return self.get_response(request)
