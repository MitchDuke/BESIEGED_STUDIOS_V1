from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """User dashboard after login"""
    return render(request, 'accounts/dashboard.html')
