from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from allauth.account.views import LogoutView as AllauthLogoutView
from allauth.account.views import ConfirmEmailView


class CustomLogoutView(AllauthLogoutView):
    template_name = "account/logout.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        list(messages.get_messages(request))
        messages.success(request, "You have been logged out successfully.")

        return response


@method_decorator(login_required, name='dispatch')
class ResendEmailConfirmationView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        email_address = EmailAddress.objects.filter(user=user, verified=False).first()
        if email_address:
            send_email_confirmation(request, user)
            messages.success(request, f"A new confirmation email has been sent to {email_address.email}.")
        else:
            messages.info(request, "Your email is already verified.")
        return redirect(reverse("account_email_verification_sent"))


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'allauth/account/email_confirm.html'
