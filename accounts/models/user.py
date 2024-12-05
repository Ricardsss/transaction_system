from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("teller", "Teller"),
        ("admin", "Admin"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")

    def is_customer(self):
        return self.role == "customer"

    def is_teller(self):
        return self.role == "teller"

    def is_admin(self):
        return self.role == "admin"

    def __str__(self):
        return self.username
