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
                'single_mini': 50.00,
                'squad': 100.00,
                'colossal': 200.00,
                'terrain': 50.00,
            }

            # Assign base price based on selected category
            category = form.cleaned_data['category']
            base_price = category_price.get(category, 0.00)

            # Calculate any additional costs
            assembly_cost = 20.00 if form.cleaned_data['assembly_required'] else 0.00
            priming_cost = 15.00 if form.cleaned_data['priming_required'] else 0.00

            # Initialize price status
            price_status = 'ready'  # Default status for ready quotes

            # Calculate percentage uplift for the size
            size_option = form.cleaned_data.get('size_option', '')
            size_uplift = 0
            if size_option == "monster":
                size_uplift = 0.5  # Example: 50% uplift for "Monster"
            elif size_option == "tank":
                size_uplift = 0.75  # Example: 75% uplift for "Tank/Walker"
            elif size_option == "colossal_monster":
                size_uplift = 2.0  # Example: 200% uplift for "Colossal Monster"
            elif size_option == "colossal_vehicle":
                size_uplift = 2.0  # Example: 200% uplift for "Colossal Vehicle"
            elif size_option == "6_10":
                size_uplift = 0.5  # Example: 50% uplift for "6 to 10 models"
            elif size_option == "11_15":
                size_uplift = 1.0  # Example: 100% uplift for "11 to 15 models"
            elif size_option == "16_20":
                size_uplift = 1.5  # Example: 150% uplift for "16 to 20 models"
            elif size_option == "21_plus" or size_option == "over_20cm" or size_option == "50cm":
                # Handle case by case for large squads, models or terrain
                size_uplift = 0.0  # Price is panding manual quote
                price_status = 'pending'
            else:
                price_status = 'ready'  # Default status for other sizes
            # Add other size options if required...

            # Apply the size uplift percentage
            uplift_amount = base_price * size_uplift

            # Calculate total price
            if price_status == 'pending':
                total_price = 0
            else:
                total_price = base_price + assembly_cost + priming_cost + uplift_amount

            # Save the commission quote
            quote = form.save(commit=False)
            quote.user = request.user
            quote.base_price = base_price
            quote.assembly_cost = assembly_cost
            quote.priming_cost = priming_cost
            quote.size_uplift = uplift_amount  # Save uplift for reference
            quote.total_price = total_price  # Update the total price
            quote.status = price_status  # Set status to 'pending' or 'ready'

            print(f"Saving quote: {quote}")

            quote.save()

            # Redirect to the commission detail page after saving
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f"Commission context: {context}")  # Add this to debug the context being passed
        return context


@login_required
def smart_commission_redirect(request):
    # Redirects user to the dashboard if they have commissions, otherwise to create a new commission
    # user = request.user
    # has_commissions = CommissionQuote.objects.filter(user=user).exists()

    # if has_commissions:
    # return redirect('dashboard')
    return redirect('commissions:create_commission')


@login_required
def delete_commission(request, pk):
    # Deletes a commission quote if it belongs to the user
    commission = CommissionQuote.objects.get(pk=pk)
    if commission.user == request.user:
        commission.delete()
    return redirect('dashboard:dashboard')


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
