from django.urls import path, include
from .views import dashboard
from .views import CustomLogoutView

urlpatterns = [
    path("logout/", CustomLogoutView.as_view(), name="account_logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("", include("allauth.urls")),  # Redirects to Allauth
]
