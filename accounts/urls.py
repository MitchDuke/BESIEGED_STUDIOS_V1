from django.urls import path, include
from .views import CustomLogoutView
# from .views import ResendEmailConfirmationView, CustomConfirmEmailView, PublicResendEmailView

app_name = "accounts"

urlpatterns = [
    path("logout/", CustomLogoutView.as_view(), name="account_logout"),

    # --- Email Verification Routes (Commented Out for Future Use) ---
    # path("resend-confirmation/", ResendEmailConfirmationView.as_view(), name="resend_email"),
    # path("confirm-email/<key>/", CustomConfirmEmailView.as_view(), name="account_confirm_email"),
    # path("resend-verification/", PublicResendEmailView.as_view(), name="public_resend_email"),

    # Allauth default auth URLs (login, register, password reset, etc.)
    path("", include("allauth.urls")),
]
