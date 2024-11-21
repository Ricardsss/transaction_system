from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ("savings", "Savings"),
        ("checking", "Checking"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_type.capitalize()} Account"
