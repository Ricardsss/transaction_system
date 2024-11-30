from django.db import models
from datetime import timedelta
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
    start_date = models.DateField(default=now)
    end_date = models.DateField(null=True, blank=True)
    last_executed = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    def next_execution_date(self):
        if not self.last_executed:
            return self.start_date
        frequency_map = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(days=30),
            "yearly": timedelta(days=365),
        }
        return self.last_executed + frequency_map[self.frequency]

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValueError("End date cannot be earlier than the start date.")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def execute(self):
        pass

    def __str__(self):
        return f"Recurring {self.amount} {self.frequency}"
