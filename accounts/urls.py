from django.urls import path, include
from .views import CustomLogoutView, ResendEmailConfirmationView, CustomConfirmEmailView

app_name = "accounts"

urlpatterns = [
    path("logout/", CustomLogoutView.as_view(), name="account_logout"),
    path("resend-confirmation/", ResendEmailConfirmationView.as_view(), name="resend_email"),
    path("confirm-email/<key>/", CustomConfirmEmailView.as_view(), name="account_confirm_email"),
    path("", include("allauth.urls")),  # Redirects to Allauth for login/register
]
