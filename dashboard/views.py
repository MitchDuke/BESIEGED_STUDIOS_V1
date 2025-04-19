from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from checkout.models import Order


@login_required
def dashboard(request):
    profile = getattr(request.user, "userprofile", None)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        "profile": profile,
        "orders": orders,
        "commissions": [],  # Replace later
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def order_detail(request, order_id):
    order = Order.objects.filter(user=request.user, id=order_id).first()
    if not order:
        return render(request, "dashboard/order_not_found.html")

    return render(request, "dashboard/order_detail.html", {"order": order})
