from django.shortcuts import render
from .models import Item
from django.contrib.auth.decorators import login_required


@login_required
def items(request):
    items = Item.objects.order_by("name")
    return render(
        request,
        "items/items.html",
        {
            "items": items,
        },
    )
