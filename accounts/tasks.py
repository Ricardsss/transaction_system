from celery import shared_task
from datetime import date

from .models import RecurringTransaction
from .utils import complete_transfer


@shared_task()
def process_recurring_transactions():
    today = date.today()
    transactions = RecurringTransaction.objects.filter(
        is_active=True, start_date__lte=today
    )

    for transaction in transactions:
        next_date = transaction.next_execution_date()
        if next_date <= today:
            complete_transfer(
                transaction.source_account.id,
                transaction.destination_account.id,
                transaction.amount,
                transaction.user,
            )
            transaction.last_executed = today
            transaction.save()
