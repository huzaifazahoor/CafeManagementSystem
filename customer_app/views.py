from django.shortcuts import render, redirect
from .models import Customer
from django.contrib.auth.decorators import login_required


@login_required
def customers(request):
    customers = Customer.objects.order_by("name")
    return render(
        request,
        "customers/customers.html",
        {
            "customers": customers,
        },
    )
