from django.urls import path
from . import views

urlpatterns = [
    path("", views.orders, name="orders"),
    path("add", views.add_order, name="add_order")
]
