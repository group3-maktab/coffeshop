import uuid
from django.db import models
from django.db.models import Sum, F

from core.models import BaseModel
from foodmenu.models import Food
from tables.models import Table


# Create your models here.


class Order(BaseModel):
    status_fields = [("W", "Waiting"),
                     ("P", "Preparation"),
                     ("T", "Transmission"),
                     ("F", "Finished")]
    customer_phone = models.CharField(max_length=100, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=1, choices=status_fields, default='W')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} - {self.customer_phone} - {self.table}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Food, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    def get_cost(self):
        return self.price * self.quantity
