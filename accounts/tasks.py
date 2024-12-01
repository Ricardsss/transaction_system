from celery import shared_task
from datetime import date

from .models import RecurringTransaction


@shared_task()
def process_recurring_transactions():
    today = date.today()
    transactions = RecurringTransaction.objects.filter(
        is_active=True, start_date__lte=today
    )

    for transaction in transactions:
        next_date = transaction.next_execution_date()
        if next_date <= today:
            print(
                f"Processing transaction {transaction.id} for user {transaction.user.id}"
            )

            transaction.last_executed = today
            transaction.save()
