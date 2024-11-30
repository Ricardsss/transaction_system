from .validators import (
    validate_input,
    validate_role,
    validate_status,
    validate_account_data,
    validate_frequency,
)


def get_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")
