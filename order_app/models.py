from django.db import models
from customer_app.models import Customer
from item_app.models import Item


CHOICES = (
    ("Breakfast", "Breakfast"),
    ("Lunch", "Lunch"),
    ("Dinner", "Dinner"),
)


class Order(models.Model):
    order_id = models.CharField(
        max_length=100,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customers",
    )
    menu = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="items",
    )
    quantity = models.IntegerField(default=1)
    time_period = models.CharField(
        max_length=15,
        choices=CHOICES,
        default="Morning",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer} - {self.menu} - {self.created_at}"
