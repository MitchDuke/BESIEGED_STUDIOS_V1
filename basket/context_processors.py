from gallery.models import Project


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
            })
        except Project.DoesNotExist:
            continue

    return {
        "basket_count": sum(item["quantity"] for item in basket_items),
        "basket_items": basket_items,
    }
