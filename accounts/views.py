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
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseRedirect


class CustomLogoutView(AllauthLogoutView):
    template_name = "account/logout.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        list(messages.get_messages(request))
        messages.success(request, "You have been logged out successfully.")

        return response


class ResendEmailConfirmationView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            email_address = EmailAddress.objects.filter(user=user, verified=False).first()
            if email_address:
                send_email_confirmation(request, user)
                messages.success(request, f"A new confirmation email has been sent to {email_address.email}.")
            else:
                messages.info(request, "Your email is already verified.")
        else:
            messages.error(request, "You must be logged in to resend verification.")
        return redirect("account_email_verification_sent")


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirm.html'

    def get_object(self, queryset=None):
        # Needed to support both HMAC and database-stored links
        key = self.kwargs.get("key")
        self.confirmation = EmailConfirmationHMAC.from_key(key)
        if not self.confirmation:
            self.confirmation = EmailConfirmation.objects.filter(key=key.lower()).first()
        return self.confirmation

    def get(self, *args, **kwargs):
        confirmation = self.get_object()
        if confirmation:
            confirmation.confirm(self.request)
            return HttpResponseRedirect(self.get_redirect_url())
        return super().get(*args, **kwargs)

    def get_redirect_url(self):
        return reverse('account_login')
