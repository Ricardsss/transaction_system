from django.db import models
from django.utils.timezone import now
from django.db import transaction
import uuid
import random

from .user import User


def random_account_number():
    return str(random.randint(100000000000, 999999999999))


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
    account_number = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        default=random_account_number,
    )
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPES,
        blank=True,
        default="savings",
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        default=0.0,
    )
    currency = models.CharField(max_length=3, blank=True, default="CAD")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, blank=True, default="active"
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["account_number"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"ID: {self.id} - Account Number: {self.account_number} - Account Type: {self.account_type}"

    @transaction.atomic
    def deposit(self, amount):
        if self.status == "closed":
            raise ValueError("Account is closed, cannot perform a deposit.")
        if self.status == "inactive":
            self.status = "active"
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()

    @transaction.atomic
    def withdraw(self, amount):
        if self.status == "closed" or self.status == "inactive":
            raise ValueError("Account must be active to complete a withdrawal.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.save()

    def close_account(self):
        if self.balance > 0:
            raise ValueError("Cannot close an account with a positive balance.")
        self.status = "closed"
        self.save()
