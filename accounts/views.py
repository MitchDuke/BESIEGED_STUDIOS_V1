from django.contrib import messages
from allauth.account.views import LogoutView as AllauthLogoutView


class CustomLogoutView(AllauthLogoutView):
    template_name = "account/logout.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        list(messages.get_messages(request))
        messages.success(request, "You have been logged out successfully.")

        return response
