from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommissionQuoteForm


@login_required
def create_commission_quote(request):
    if request.method == 'POST':
        form = CommissionQuoteForm(request.POST, request.FILES)
        if form.is_valid():
            commission = form.save(commit=False)
            commission.user = request.user
            commission.save()
            return redirect('dashboard')  # or a 'commission_detail' view
    else:
        form = CommissionQuoteForm()
    return render(request, 'commissions/commissions_form.html', {'form': form})
