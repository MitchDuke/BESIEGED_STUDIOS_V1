from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order
from commissions.models import CommissionQuote


@login_required
def dashboard(request):
    profile = getattr(request.user, "userprofile", None)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    commissions = CommissionQuote.objects.filter(user=request.user).order_by('-created_at')

    print("Commssions: ", commissions)

    context = {
        "profile": profile,
        "orders": orders,
        "commissions": commissions,
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def order_detail(request, order_id):
    order = Order.objects.filter(user=request.user, id=order_id).first()
    if not order:
        return render(request, "dashboard/order_not_found.html")

    return render(request, "dashboard/order_detail.html", {"order": order})


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard:dashboard')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'dashboard/edit_profile.html', {'form': form})
