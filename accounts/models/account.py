from django.db import models
from django.utils.timezone import now
import uuid

from .user import User


class Account(models.Model):
    ACCOUNT_TYPES = (
        ("savings", "Savings"),
        ("checking", "Checking"),
        ("loan", "Loan"),
    )
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("closed", "Closed"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(
        max_length=10, choices=ACCOUNT_TYPES, default="savings"
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    currency = models.CharField(max_length=3, default="CAD")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(default=now)
    uodated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.account_type}"
