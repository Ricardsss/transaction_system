from django.db import models
import uuid

from .user import User
from .transaction import Transaction
from .recurring_transaction import RecurringTransaction


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    action = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="audit_logs"
    )
    recurring = models.ForeignKey(
        RecurringTransaction, on_delete=models.SET_NULL, null=True, blank=True
    )
    transaction = models.ForeignKey(
        Transaction, on_delete=models.SET_NULL, null=True, blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} by {self.user}"
