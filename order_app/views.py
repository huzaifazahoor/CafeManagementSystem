from django.shortcuts import render, redirect
from .models import Order
from item_app.models import Item
from customer_app.models import Customer
from django.contrib.auth.decorators import login_required
import uuid
from django.db.models import Count, Sum


@login_required
def orders(request):
    orders = Order.objects.values(
        "order_id", "customer__name", "created_at__date", "time_period"
    ).annotate(
        num_orders=Count("id"),
        total_price=Sum("menu__price"),
    )
    print(orders)
    return render(request, "orders/orders.html", {"orders": orders})


@login_required
def add_order(request):
    if request.method == "POST":
        if customer := request.POST.get("customer") or None:
            order_id = str(uuid.uuid4())
            cust = Customer.objects.get(pk=int(customer))
            time_period = request.POST.get("time_period") or None
            quantities = request.POST.getlist("quantity")
            flags = request.POST.getlist("flag")
            flags = {flag: True for flag in flags}
            items = request.POST.getlist("item")
            for item, quantity in zip(items, quantities):
                flag = flags.get(item) or False
                if flag:
                    menu = Item.objects.get(name=item.strip())
                    obj, created = Order.objects.update_or_create(
                        customer=cust,
                        order_id=order_id,
                        menu=menu,
                        defaults={
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


def edit_order(request):
    if order_id := request.GET.get("order-num") or None:
        orders = Order.objects.prefetch_related("customer").filter(
            order_id=order_id,
        )
        if len(orders) > 0:
            return render(request, "orders/edit_order.html", {"orders": orders})
    return redirect("orders")
