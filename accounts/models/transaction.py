from django.db import models
from django.utils.timezone import now


from .account import BankAccount


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("transfer", "Transfer"),
    ]
    account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(default=now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            f"{self.transaction_type.capitalize()} of {self.amount} on {self.account}"
        )
