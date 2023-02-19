from django.shortcuts import render, redirect
from .models import Order
from django.db.models import Sum, F
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
    if request.method == "POST":
        if customer := request.POST.get("customer") or None:
            cust = Customer.objects.get(pk=int(customer))
            time_period = request.POST.get("time_period") or None
            quantities = request.POST.getlist("quatity")
            flags = request.POST.getlist("flag")
            items = request.POST.getlist("item")
            for item, quantity, flag in zip(items, quantities, flags):
                if flag:
                    menu = Item.objects.get(name=item.strip())
                    obj, created = Item.objects.update_or_create(
                        customer=cust,
                        order_id="order_id",
                        defaults={
                            "menu": menu,
                            "quantity": int(quantity),
                            "time_period": time_period,
                        },
                    )
            return redirect("orders")
    context = {
        "items": Item.objects.filter(is_available=True),
        "customers": Customer.objects.order_by("name"),
    }
    return render(request, "orders/add_order.html", context=context)
