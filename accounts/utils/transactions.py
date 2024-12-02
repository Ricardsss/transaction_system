from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404

from ..models import Account, Transaction, AuditLog


def get_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")


def complete_transfer(source_account_id, destination_account_id, amount, user):
    source_account = get_object_or_404(Account, pk=source_account_id)
    destination_account = get_object_or_404(Account, pk=destination_account_id)
    with db_transaction.atomic():
        source_account.withdraw(amount)
        source_account.save()
        destination_account.deposit(amount)
        destination_account.save()
    transaction = Transaction.objects.create(
        user=user,
        source_account=source_account,
        destination_account=destination_account,
        transaction_type="transfer",
        amount=amount,
    )
    transaction.save()
    AuditLog.objects.create(
        action="Recurring Transaction",
        transaction=transaction,
        details={
            "amount": str(amount),
            "sender": str(source_account),
            "receiver": str(destination_account),
        },
    )
    return transaction
