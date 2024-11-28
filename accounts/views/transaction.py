from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction
from decimal import Decimal
import json

from ..models import Account, Transaction, AuditLog
from ..utils import validate_role, validate_input, get_ip_address


class DepositView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        if not validate_role(user.role):
            return JsonResponse({"error": "Permission denied."}, status=403)
        try:
            data = json.loads(request.body) if request.body else {}
            errors = validate_input(data, ["amount"])
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            amount = Decimal(data["amount"])
            account = get_object_or_404(Account, pk=pk, user=user)
            account.deposit(amount)
            account.save()
            transaction = Transaction.objects.create(
                source_account=account,
                transaction_type="deposit",
                amount=amount,
            )
            ip_address = get_ip_address(request)
            AuditLog.objects.create(
                user=user,
                action="User Deposit",
                transaction=transaction,
                ip_address=ip_address,
                details={"amount": str(amount), "account": str(account)},
            )
            return JsonResponse(
                {"message": "Deposit successful.", "balance": account.balance},
                status=200,
            )
        except Exception as e:
            if type(e) == ValueError:
                return JsonResponse({"error": str(e)}, status=400)
            return JsonResponse({"error": str(e)}, status=500)


class WithdrawView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        if not validate_role(user.role):
            return JsonResponse({"error": "Permission denied."}, status=403)
        try:
            data = json.loads(request.body) if request.body else {}
            errors = validate_input(data, ["amount"])
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            amount = Decimal(data["amount"])
            account = get_object_or_404(Account, pk=pk, user=user)
            account.withdraw(amount)
            transaction = Transaction.objects.create(
                source_account=account,
                transaction_type="withdrawal",
                amount=amount,
            )
            ip_address = get_ip_address(request)
            AuditLog.objects.create(
                user=user,
                action="User Withdrawal",
                transaction=transaction,
                ip_address=ip_address,
                details={"amount": str(amount), "account": str(account)},
            )
            return JsonResponse(
                {"message": "Withdrawal successful.", "balance": account.balance},
                status=200,
            )
        except Exception as e:
            if type(e) == ValueError:
                return JsonResponse({"error": str(e)}, status=400)
            return JsonResponse({"error": str(e)}, status=500)


class TransferView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        if not validate_role(user.role):
            return JsonResponse({"error": "Permission denied."}, status=403)
        try:
            data = json.loads(request.body) if request.body else {}
            errors = validate_input(
                data, ["amount", "source_account_id", "destination_account_id"]
            )
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            amount = Decimal(data["amount"])
            source_account_id = data["source_account_id"]
            destination_account_id = data["destination_account_id"]
            source_account = get_object_or_404(Account, pk=source_account_id, user=user)
            destination_account = get_object_or_404(Account, pk=destination_account_id)
            with db_transaction.atomic():
                source_account.withdraw(amount)
                source_account.save()
                destination_account.deposit(amount)
                destination_account.save()
            transaction = Transaction.objects.create(
                source_account=source_account,
                destination_account=destination_account,
                transaction_type="transfer",
                amount=amount,
            )
            ip_address = get_ip_address(request)
            AuditLog.objects.create(
                user=user,
                action="Transfer",
                transaction=transaction,
                ip_address=ip_address,
                details={
                    "amount": str(amount),
                    "sender": str(source_account),
                    "receiver": str(source_account),
                },
            )
            return JsonResponse({"message": "Transfer successful."}, status=200)
        except Exception as e:
            if type(e) == ValueError:
                return JsonResponse({"error": str(e)}, status=400)
            return JsonResponse({"error": str(e)}, status=500)
