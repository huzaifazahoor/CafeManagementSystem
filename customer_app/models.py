from django.db import models


class Customer(models.Model):
    cnic = models.CharField(max_length=13)
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
