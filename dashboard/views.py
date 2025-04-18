from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile


@login_required
def dashboard(request):
    profile = None
    try:
        profile = request.user.userprofile
    except Exception:
        pass

    context = {
        "profile": profile,
        # Placeholder for later:
        "orders": [],  # You'll replace with order query
        "commissions": [],  # Replace later
    }

    return render(request, 'dashboard/dashboard.html', context)
