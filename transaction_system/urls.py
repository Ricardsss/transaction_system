from django.contrib import admin
from django.urls import path, include

from accounts.views import RegisterView, LoginView, LogoutView
from .views import set_csrftoken


urlpatterns = [
    path("", set_csrftoken, name="token"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
]
