from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
import json

from ..models import Dispute, Transaction
from ..utils import validate_input, validate_dispute_status, validate_dispute_reason
from ..decorators import roles_required


class DisputeListCreateView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            user = request.user
            if user.is_teller() or user.is_admin():
                disputes = Dispute.objects.all()
            else:
                disputes = Dispute.objects.filter(user=user)
            disputes_data = [
                {
                    "id": str(dispute.id),
                    "transaction_id": str(dispute.transaction.id),
                    "reason": dispute.reason,
                    "status": dispute.status,
                    "created_at": dispute.created_at,
                }
                for dispute in disputes
            ]
            return JsonResponse({"disputes": disputes_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body) if request.body else {}
            errors = validate_input(data, ["transaction"])
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            if "reason" in data and not validate_dispute_reason(data["reason"]):
                return JsonResponse(
                    {
                        "error": "Invalid reason. Must be unauthorized_charge, duplicate_transaction, service_not_received, or other."
                    },
                    status=400,
                )
            transaction = get_object_or_404(
                Transaction, id=data["transaction"], user=user
            )
            data["transaction"] = transaction
            data["user"] = user
            dispute = Dispute(**data)
            dispute.save()
            return JsonResponse(
                {"message": "Dispute created successfully!", "dispute": dispute.id}
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(roles_required(["teller", "admin"]), name="dispatch")
class DisputeUpdateView(LoginRequiredMixin, View):
    def patch(self, request, pk):
        try:
            data = json.loads(request.body) if request.body else {}
            errors = validate_input(data, ["status"])
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            if not validate_dispute_status(data["status"]):
                return JsonResponse(
                    {
                        "error": "Invalid status. Must be open, in_progress, resolved, or rejected."
                    },
                    status=400,
                )
            dispute = get_object_or_404(Dispute, pk=pk)
            dispute.status = data["status"]
            dispute.resolution_details = data.get("resolution_details", "")
            dispute.save()
            return JsonResponse(
                {"message": "Dispute updated successfully."}, status=200
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
