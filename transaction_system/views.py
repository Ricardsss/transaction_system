from django.http import JsonResponse


def set_csrftoken(request):
    return JsonResponse({"message": "Setting CSRF Token"}, status=200)
