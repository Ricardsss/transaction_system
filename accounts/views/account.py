from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json


from ..models import Account, AuditLog
from ..utils import validate_account_data, validate_input, validate_status


class AccountListCreateView(LoginRequiredMixin, View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        account_data = [
            {
                "id": account.id,
                "account_number": account.account_number,
                "account_type": account.account_type,
                "balance": account.balance,
                "currency": account.currency,
                "status": account.status,
                "created_at": account.created_at,
            }
            for account in accounts
        ]
        return JsonResponse({"accounts": account_data})

    def post(self, request):
        data = json.loads(request.body) if request.body else {}
        validation_errors = validate_account_data(data)
        if validation_errors:
            return JsonResponse({"errors": validation_errors}, status=400)
        data["user"] = request.user
        account = Account(**data)
        account.save()
        return JsonResponse(
            {"message": "Account created successfully!", "account_id": account.id},
            status=201,
        )


class AccountDetailUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        account_data = {
            "id": account.id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "balance": account.balance,
            "currency": account.currency,
            "status": account.status,
            "created_at": account.created_at,
        }
        return JsonResponse(account_data)

    def patch(self, request, pk):
        data = json.loads(request.body) if request.body else {}
        account = get_object_or_404(Account, pk=pk, user=request.user)
        errors = validate_input(data, ["status"])
        if errors:
            return JsonResponse({"errors": errors}, status=400)
        if not validate_status(data["status"]):
            return JsonResponse(
                {"error": "Invalid status value. Must be active, inactive, or closed."},
                status=400,
            )
        if data["status"] == "closed":
            try:
                account.close_account()
                account.save()
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            account.status = data["status"]
            account.save()
        return JsonResponse({"message": "Account updated successfully!"}, status=200)
