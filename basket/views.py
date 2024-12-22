from django.shortcuts import render, redirect
from django.contrib import messages
from gallery.models import Project


def basket_view(request):
    basket = request.session.get("basket", {})
    basket_items = []
    for pk, quantity in basket.items():
        try:
            project = Project.objects.get(pk=int(pk))
            basket_items.append({
                "project": project,
                "quantity": quantity,
                'total_price': project.price * quantity
            })
        except Project.DoesNotExist:
            continue
    return render(request, "basket/basket.html", {"basket": basket, "basket_items": basket_items})


def add_to_basket(request, pk):
    basket = request.session.get("basket", {})
    if pk in basket:
        basket[pk] += 1
    else:
        basket[pk] = 1
    request.session["basket"] = basket
    messages.success(request, "Item added to basket.")
    return redirect("basket:basket_view")


def update_basket(request, pk, action):
    basket = request.session.get("basket", {})
    pk = str(pk)
    if pk in basket:
        if action == "add":
            basket[pk] += 1
        elif action == "reduce":
            basket[pk] = max(1, basket[pk] - 1)
        elif action == "remove":
            del basket[pk]
    request.session["basket"] = basket
    return redirect("basket:basket_view")
