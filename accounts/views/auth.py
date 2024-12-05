from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db import IntegrityError
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging


from ..utils import validate_input, validate_role, get_ip_address
from ..models import AuditLog, User

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.body else {}
            errors = validate_input(data, ["username", "email", "password", "role"])
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            try:
                validate_email(data["email"])
            except ValidationError:
                return JsonResponse({"error": "Invalid email format."}, status=400)
            if not validate_role(data["role"]):
                return JsonResponse({"error": "Invalid role specified"}, status=400)
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                role=data["role"],
            )
            user.save()
            ip_address = get_ip_address(request)
            AuditLog.objects.create(
                user=user,
                ip_address=ip_address,
                action="User Registered",
                details={"username": data["username"]},
            )
            return JsonResponse(
                {"message": "User registered successfully!", "user": user.id},
                status=201,
            )
        except IntegrityError as e:
            return JsonResponse(
                {"error": "Username or email already exists."}, status=400
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.body else {}
            errors = validate_input(data, ["username", "password"])
            if errors:
                return JsonResponse({"errors": errors}, status=400)

            username = data["username"]
            password = data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                ip_address = get_ip_address(request)
                AuditLog.objects.create(
                    user=user,
                    ip_address=ip_address,
                    action="User Login",
                    details={"username": username},
                )
                return JsonResponse({"message": "Login successful"})
            return JsonResponse({"error": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Internal server error"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(LoginRequiredMixin, View):
    def delete(self, request):
        logger.info(f"Referer: {request.headers.get('Referer')}")
        logger.info("CSRF" + request.COOKIES.get("csrftoken"))
        logger.info("Token" + request.headers.get("X-CSRFToken"))
        user = request.user
        logout(request)
        ip_address = get_ip_address(request)
        AuditLog.objects.create(
            user=user,
            ip_address=ip_address,
            action="User Logout",
            details={"username": user.username},
        )
        return JsonResponse({"message": "Logout successful"})
