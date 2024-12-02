from django.db import models
from django.utils.timezone import now
import uuid

from .transaction import Transaction
from .user import User


class Dispute(models.Model):
    STATUS_CHOICES = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("rejected", "Rejected"),
    )
    REASON_CHOICES = (
        ("unauthorized_charge", "Unauthorized Charge"),
        ("duplicate_transaction", "Duplicate Transaction"),
        ("service_not_received", "Service Not Received"),
        ("other", "Other"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="disputes"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disputes")
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, default="other")
    additional_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="open")
    resolution_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Dispute {self.id} - {self.status}"
