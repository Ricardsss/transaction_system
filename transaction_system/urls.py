from django.contrib import admin
from django.urls import path, include

from .views import set_csrftoken


urlpatterns = [
    # Only used in development
    path("", set_csrftoken, name="token"),
    path("admin/", admin.site.urls),
]
