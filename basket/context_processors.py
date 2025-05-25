from gallery.models import Project
from commissions.models import CommissionQuote


def basket_context(request):
    """Context processor to add basket data globally."""
    basket = request.session.get("basket", {})
    basket_items = []
    for pk, quantity in basket.items():
        try:
            project = Project.objects.get(pk=int(pk))
            basket_items.append({
                "project": project,
                "quantity": quantity,
                "total_price": project.price * quantity,
                "is_commission": False
            })
        except Project.DoesNotExist:
            try:
                commission = CommissionQuote.objects.get(pk=int(pk))
                basket_items.append({
                    "project": commission,
                    "quantity": quantity,
                    "total_price": commission.total_price * quantity,
                    "is_commission": True
                })
            except CommissionQuote.DoesNotExist:
                # If neither Project nor CommissionQuote exists, skip this item
                continue

    return {
        "basket_count": sum(item["quantity"] for item in basket_items),
        "basket_items": basket_items,
    }
