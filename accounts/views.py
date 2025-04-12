from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.views import LogoutView as AllauthLogoutView


@login_required
def dashboard(request):
    """User dashboard after login"""
    return render(request, 'accounts/dashboard.html')


class CustomLogoutView(AllauthLogoutView):
    template_name = "account/logout.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, "You have been logged out successfully.")
        return response
