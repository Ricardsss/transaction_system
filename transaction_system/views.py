from django.http import JsonResponse


# Only used in development
def set_csrftoken(request):
    return JsonResponse({"message": "Setting CSRF Token in development"}, status=200)
