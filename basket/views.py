from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gallery.models import Project
from commissions.models import CommissionQuote


def basket_view(request):
    """Render basket page and update dropdown contents."""
    basket = request.session.get('basket', {})
    basket_items = []

    for pk, quantity in basket.items():
        try:
            project = Project.objects.get(pk=int(pk))
            basket_items.append({
                "project": project,
                "quantity": quantity,
                "total_price": project.price * quantity,
            })
        except Project.DoesNotExist:
            try:
                commission = CommissionQuote.objects.get(pk=int(pk))
                basket_items.append({
                    "project": commission,
                    "quantity": quantity,
                    "total_price": commission.total_price * quantity,
                    "is_commission": True,
                })
            except CommissionQuote.DoesNotExist:
                continue

    return render(request, "basket/basket.html", {"basket_items": basket_items})


def adjust_basket(request, pk):
    """Update item quantity in the basket."""
    project = get_object_or_404(Project, pk=pk)
    quantity = int(request.POST.get("quantity", 1))
    basket = request.session.get("basket", {})

    if quantity > 0:
        basket[str(pk)] = quantity
        messages.success(request, f"Updated {project.title} quantity to {quantity}")
    else:
        basket.pop(str(pk), None)
        messages.success(request, f"Removed {project.title} from your basket")

    request.session["basket"] = basket
    return redirect(request.META.get("HTTP_REFERER", "basket:basket_view"))


def remove_from_basket(request, pk):
    """Remove an item from the basket."""
    basket = request.session.get("basket", {})
    basket.pop(str(pk), None)
    request.session["basket"] = basket
    messages.success(request, "Item removed.")
    return redirect(request.META.get("HTTP_REFERER", "basket:basket_view"))
