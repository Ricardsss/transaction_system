from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db import IntegrityError
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

from ..utils.validators import validate_input, validate_role
from ..models import AuditLog, User


class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            errors = validate_input(data, ["username", "email", "password", "role"])
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            try:
                validate_email(data["email"])
            except ValidationError:
                return JsonResponse({"error": "Invalid email format."}, status=400)
            if validate_role(data["role"]):
                return JsonResponse({"error": "Invalid role specified"}, status=400)
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                role=data["role"],
            )
            return JsonResponse(
                {"message": "User registered successfully!", "user_id": user.id},
                status=201,
            )
        except IntegrityError as e:
            return JsonResponse(
                {"error": "Username or email already exists."}, status=400
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        errors = validate_input(data, ["username", "password"])
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        username = data["username"]
        password = data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            AuditLog.objects.create(
                user=user, action="User Login", details={"username": username}
            )
            return JsonResponse({"message": "Login successful"})
        return JsonResponse({"error": "Invalid credentials"}, status=400)


class LogoutView(View):
    @method_decorator(login_required)
    def delete(self, request):
        user = request.user
        logout(request)
        AuditLog.objects.create(
            user=user, action="User Logout", details={"username": user.username}
        )
        return JsonResponse({"message": "Logout successful"})
