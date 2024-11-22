from django.contrib import admin

from .models import User, Account, Transaction, AuditLog, Dispute, RecurringTransaction

# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(AuditLog)
admin.site.register(Dispute)
admin.site.register(RecurringTransaction)
