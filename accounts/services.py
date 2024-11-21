from django.db import transaction
from .models import BankAccount, Transaction


def process_transaction(account_id, transaction_type, amount, description=""):
    with transaction.atomic():
        account = BankAccount.objects.select_for_update().get(id=account_id)

        if transaction_type == "withdrawal" and account.balance < amount:
            raise ValueError("Insufficient funds")

        if transaction_type == "deposit":
            account.balance += amount
        elif transaction_type == "withdrawal":
            account.balance -= amount

        account.save()

        return Transaction.objects.create(
            account=account,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
        )
