from django.shortcuts import render
from .models import Order
from django.db.models import Sum, Case, CharField, Value, When, F
from datetime import datetime
from item_app.models import Item
from customer_app.models import Customer
from django.contrib.auth.decorators import login_required


@login_required
def orders(request):
    orders = (
        Order.objects.annotate(
            order_total=Sum(F("quantity") * F("menu__price")),
            order_items=F("menu__name"),
        )
        .filter(created_at__date=datetime.now().date())
        .values(
            "id",
            "customer__name",
            "order_total",
            "order_items",
            "time_period",
            "created_at__date",
        )
        .order_by("created_at__date", "time_period")
    )
    print(orders)
    return render(
        request,
        "orders/orders.html",
    )


@login_required
def add_order(request):
    context = {
        "items": Item.objects.filter(is_available=True),
        "customers": Customer.objects.order_by("name"),
    }
    return render(request, "orders/add_order.html", context=context)
