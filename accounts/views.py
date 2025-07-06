from django.contrib import messages
from django.shortcuts import redirect
from allauth.account.views import LogoutView as AllauthLogoutView


# Custom logout view to show success message
class CustomLogoutView(AllauthLogoutView):
    template_name = "account/logout.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        list(messages.get_messages(request))  # Clears any old messages
        messages.success(request, "You have been logged out successfully.")
        return response


# --- Email Verification System (Commented Out for Future Use) ---
"""
from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from django.views import View
from django.http import HttpResponseRedirect, Http404
from allauth.account.views import ConfirmEmailView


class EmailResendForm(forms.Form):
    email = forms.EmailField(label="Your email address")


class PublicResendEmailView(FormView):
    template_name = "account/public_resend_email.html"
    form_class = EmailResendForm
    success_url = "/accounts/verification-sent/"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        email_address = EmailAddress.objects.filter(email=email, verified=False).first()

        if email_address:
            send_email_confirmation(self.request, email_address.user)
            messages.success(self.request, f"A confirmation email has been resent to {email}.")
        else:
            messages.info(self.request, "This email is already verified or not registered.")

        return super().form_valid(form)


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

    def get(self, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            raise Http404("Invalid confirmation key.")

        self.object.confirm(self.request)  # Marks email as verified
        return HttpResponseRedirect(self.get_redirect_url())

    def get_object(self, queryset=None):
        key = self.kwargs.get("key")
        confirmation = EmailConfirmationHMAC.from_key(key)

        if not confirmation:
            try:
                confirmation = EmailConfirmation.objects.get(key__iexact=key)
            except EmailConfirmation.DoesNotExist:
                confirmation = None

        return confirmation
"""
