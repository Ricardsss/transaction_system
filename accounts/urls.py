from django.urls import path
from .views import (
    AccountListCreateView,
    AccountDetailUpdateView,
    DepositView,
    WithdrawView,
    TransferView,
    RecurringTransactionListCreateView,
    RecurringTransactionUpdateCancelView,
)


urlpatterns = [
    path("", AccountListCreateView.as_view(), name="account_list_create"),
    path("<uuid:pk>/", AccountDetailUpdateView.as_view(), name="account_detail_update"),
    path("transactions/deposit/<uuid:pk>/", DepositView.as_view(), name="deposit"),
    path("transactions/withdraw/<uuid:pk>/", WithdrawView.as_view(), name="withdraw"),
    path("transactions/transfer/", TransferView.as_view(), name="transfer"),
    path(
        "recurring/",
        RecurringTransactionListCreateView.as_view(),
        name="recurring_list_create",
    ),
    path(
        "recurring/<uuid:pk>/",
        RecurringTransactionUpdateCancelView.as_view(),
        name="recurring_update_cancel",
    ),
]
