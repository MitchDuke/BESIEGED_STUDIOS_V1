from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("", include("allauth.urls")),  # Redirects to Allauth
]
