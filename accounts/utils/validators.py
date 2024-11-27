from ..models import User


def validate_input(data, required_fields):
    errors = {}
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f"{field} is required."
    return errors


def validate_role(role):
    return role not in dict(User.ROLE_CHOICES)


def validate_account_data(data):
    errors = {}
    if "account_type" in data and data["account_type"] not in [
        "savings",
        "checking",
        "loan",
    ]:
        errors["account_type"] = (
            "Invalid account type. Must be savings, checking, or loan."
        )
    if "balance" in data:
        try:
            balance = float(data["balance"])
            if balance < 0:
                errors["balance"] = "Balance cannot be negative."
        except ValueError:
            errors["balance"] = "Balance must be a numeric value."
    if "currency" in data and data["currency"] not in ["CAD", "USD", "EUR", "GBP"]:
        errors["currency"] = "Unsupported currency. Must be CAD USD, EUR, or GBP."
    if "status" in data and data["status"] not in ["active", "inactive", "closed"]:
        errors["status"] = "Invalid status. Must be active, inactive, or closed"
    return errors
