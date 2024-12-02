from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from ..models import RecurringTransaction, AuditLog
from ..utils import validate_input, validate_frequency, get_ip_address


class RecurringTransactionListCreateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        transactions = RecurringTransaction.objects.filter(
            user=user, is_active=True
        ).values()
        return JsonResponse(
            {"status": "success", "transactions": list(transactions)}, status=200
        )

    def post(self, request):
        try:
            data = json.loads(request.body) if request.body else {}
            user = request.user
            errors = validate_input(
                data,
                ["source_account_id", "destination_account_id", "amount", "frequency"],
            )
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            if not validate_frequency(data["frequency"]):
                return JsonResponse(
                    {
                        "error": "Invalid frequency value. Must be daily, weekly, monthly, or yearly."
                    },
                    status=400,
                )
            data["user"] = user
            transaction = RecurringTransaction(**data)
            transaction.save()
            ip_address = get_ip_address(request)
            AuditLog.objects.create(
                user=user,
                recurring=transaction,
                action="Recurring Transaction Created",
                ip_address=ip_address,
                details={
                    "amount": str(data["amount"]),
                    "source_account": str(data["source_account_id"]),
                    "destination_account": str(data["destination_account_id"]),
                },
            )
            return JsonResponse(
                {
                    "message": "Recurring transaction created successfully!",
                    "transaction": transaction.id,
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class RecurringTransactionUpdateCancelView(LoginRequiredMixin, View):
    def patch(self, request, pk):
        try:
            data = json.loads(request.body) if request.body else {}
            user = request.user
            transaction = get_object_or_404(
                RecurringTransaction, pk=pk, user=user, is_active=True
            )
            if "frequency" in data:
                if not validate_frequency(data["frequency"]):
                    return JsonResponse(
                        {
                            "error": "Invalid frequency value. Must be daily, weekly, monthly, or yearly."
                        },
                        status=400,
                    )
                else:
                    transaction.frequency = data["frequency"]
            if "source_account" in data:
                transaction.source_account = data["source_account"]
            if "destination_account" in data:
                transaction.destination_account = data["destination_account"]
            if "amount" in data:
                transaction.amount = data["amount"]
            if "start_date" in data:
                transaction.start_date = data["start_date"]
            if "end_date" in data:
                transaction.end_date = data["end_date"]
            if "description" in data:
                transaction.description = data["description"]
            transaction.save()
            ip_address = get_ip_address(request)
            AuditLog.objects.create(
                user=user,
                recurring=transaction,
                action="Recurring Transaction Updated",
                ip_address=ip_address,
            )
            return JsonResponse(
                {"message": "Recurring transaction updated successfully!"}, status=200
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            user = request.user
            transaction = get_object_or_404(
                RecurringTransaction, pk=pk, user=user, is_active=True
            )
            transaction.is_active = False
            transaction.save()
            ip_address = get_ip_address(request)
            AuditLog.objects.create(
                user=user,
                recurring=transaction,
                action="Recurring Transaction Deleted",
                ip_address=ip_address,
            )
            return JsonResponse(
                {"message": "Transaction cancelled successfully."},
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
