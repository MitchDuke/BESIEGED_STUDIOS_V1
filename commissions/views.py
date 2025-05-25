from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CommissionQuoteForm
from django.views.generic.detail import DetailView
from .models import CommissionQuote


@login_required
def create_commission_quote(request):
    if request.method == 'POST':
        form = CommissionQuoteForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")

            # Set the base price based on the category
            category_price = {
                'single_mini': 10.00,
                'squad': 30.00,
                'colossal': 100.00,
                'terrain': 50.00,
            }

            # Assign base price based on selected category
            category = form.cleaned_data['category']
            base_price = category_price.get(category, 0.00)

            # Calculate any additional costs
            assembly_cost = 15.00 if form.cleaned_data['assembly_required'] else 0.00
            priming_cost = 5.00 if form.cleaned_data['priming_required'] else 0.00

            # Calculate total price
            total_price = base_price + assembly_cost + priming_cost

            # Save the commission quote
            quote = form.save(commit=False)
            quote.user = request.user
            quote.base_price = base_price
            quote.assembly_cost = assembly_cost
            quote.total_price = total_price

            print(f"Saving quote: {quote}")

            quote.save()

            return redirect('commissions:commissions_detail', pk=quote.pk)
        else:
            print("Form is not valid!")
            print(form.errors)
    else:
        form = CommissionQuoteForm()

    return render(request, 'commissions/commissions_form.html', {'form': form})


class CommissionQuoteDetailView(DetailView):
    model = CommissionQuote
    template_name = 'commissions/commissions_detail.html'
    context_object_name = 'commission'


@login_required
def smart_commission_redirect(request):
    # Redirects user to the dashboard if they have commissions, otherwise to create a new commission
    user = request.user
    has_commissions = CommissionQuote.objects.filter(user=user).exists()

    if has_commissions:
        return redirect('dashboard')
    return redirect('commissions:create_commission')


@login_required
def delete_commission(request, pk):
    # Deletes a commission quote if it belongs to the user
    commission = CommissionQuote.objects.get(pk=pk)
    if commission.user == request.user:
        commission.delete()
    return redirect('dashboard')


@login_required
def dashboard(request):
    commissions = CommissionQuote.objects.filter(user=request.user)
    context = {
        'commissions': commissions,
    }
    return render(request, 'dashboard.html', context)


@login_required
def add_to_basket(request, pk):
    # Adds commission to the basket
    try:
        commission = CommissionQuote.objects.get(pk=pk)
    except CommissionQuote.DoesNotExist:
        # Handle the case where the commission does not exist
        messages.error(request, "Commission not found.")
        return redirect('commissions:dashboard')

    # Initialize the basket session if it doesn't exist
    basket = request.session.get('basket', {})

    # Add the commission to the basket
    key = str(commission.pk)
    if key in basket:
        basket[key] += 1
    else:
        basket[key] = 1
    request.session['basket'] = basket

    messages.success(request, f"Commission '{commission.pk}' added to basket.")
    return redirect('checkout:checkout')
