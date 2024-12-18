from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.db.models import Sum

from ..decorators import roles_required
from ..models import Account, Transaction


class AccountStatementView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            user = request.user
            account_id = request.GET.get("account_id")
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if not start_date or not end_date:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            account = get_object_or_404(Account, id=account_id, user=user)
            outgoing_transactions = Transaction.objects.filter(
                source_account=account, created_at__range=(start_date, end_date)
            ).values("id", "transaction_type", "amount", "description", "created_at")
            incoming_transactions = Transaction.objects.filter(
                destination_account=account, created_at__range=(start_date, end_date)
            ).values("id", "transaction_type", "amount", "description", "created_at")
            response_data = {
                "account": {
                    "account_number": account.account_number,
                    "account_type": account.account_type,
                },
                "outgoing_transactions": list(outgoing_transactions),
                "incoming_transactions": list(incoming_transactions),
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(roles_required(["teller", "admin"]), name="dispatch")
class InternalReportView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            total_deposits = Transaction.objects.filter(
                transaction_type="deposit"
            ).aggregate(Sum("amount"))["amount__sum"]
            total_withdrawals = Transaction.objects.filter(
                transaction_type="withdrawal"
            ).aggregate(Sum("amount"))["amount__sum"]
            total_transfers = Transaction.objects.filter(
                transaction_type="transfer"
            ).aggregate(Sum("amount"))["amount__sum"]
            report = {
                "total_deposits": total_deposits or 0,
                "total_withdrawal": total_withdrawals or 0,
                "total_transfers": total_transfers or 0,
                "net_balance": (total_deposits or 0) - (total_withdrawals or 0),
                "transaction_count": Transaction.objects.count(),
            }
            return JsonResponse(report)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
