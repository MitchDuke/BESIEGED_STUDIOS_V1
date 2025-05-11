from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommissionQuoteForm
from django.views.generic.detail import DetailView
from .models import CommissionQuote


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


class CommissionQuoteDetailView(DetailView):
    model = CommissionQuote
    template_name = 'commissions/commission_detail.html'
    context_object_name = 'commission'


@login_required
def smart_commission_redirect(request):
    user = request.user
    has_commissions = CommissionQuote.objects.filter(user=user).exists()

    if has_commissions:
        return redirect('dashboard')
    return redirect('commissions:create_commission')
