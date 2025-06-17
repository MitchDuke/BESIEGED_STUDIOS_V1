from django.urls import path, include
from .views import CustomLogoutView
from .views import ResendEmailConfirmationView

app_name = "accounts"

urlpatterns = [
    path("logout/", CustomLogoutView.as_view(), name="account_logout"),
    path("resend-confirmation/", ResendEmailConfirmationView.as_view(), name="resend_email"),
    path("", include("allauth.urls")),  # Redirects to Allauth for login/register
]
