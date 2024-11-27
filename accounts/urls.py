from django.urls import path
from .views import AccountListCreateView, AccountDetailUpdateView


urlpatterns = [
    path("", AccountListCreateView.as_view(), name="account_list_create"),
    path("<uuid:pk>/", AccountDetailUpdateView.as_view(), name="account_detail_update"),
]
