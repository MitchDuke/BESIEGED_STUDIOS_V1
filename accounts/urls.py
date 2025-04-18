from django.urls import path, include
from .views import CustomLogoutView

urlpatterns = [
    path("logout/", CustomLogoutView.as_view(), name="account_logout"),
    path("", include("allauth.urls")),  # Redirects to Allauth for login/register
]
