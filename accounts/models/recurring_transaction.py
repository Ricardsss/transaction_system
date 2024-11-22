from django.db import models
from django.utils.timezone import now
import uuid

from .user import User
from .account import Account


class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = (
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )
    STATUS_CHOICES = (
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recurring_transactions"
    )
    source_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="recurring_outgoing"
    )
    destination_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="recurring_incoming"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    next_execution_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recurring {self.amount} {self.frequency}"
