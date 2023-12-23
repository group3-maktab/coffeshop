import uuid
from django.db import models
from django.db.models import Sum, F

from core.models import BaseModel
from foodmenu.models import Food
from tables.models import Table


# Create your models here.


class Order(BaseModel):

    status_fields = [("S", "Start"), ("W", "Waiting"),
                     ("C", "Confirmation"), ("P", "Preparation"),
                     ("T", "Transmission"), ("F", "Finished")]

    customer_phone = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=1, choices=status_fields, default='S')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(Food, through='OrderItem')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # First save the order to get an id
        self.total_price = OrderItem.objects.filter(order=self).annotate(
            total_price=F('product__price') * F('quantity')
        ).aggregate(total_price=Sum('total_price'))['total_price'] or 0
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Order #{self.id} - {self.customer_phone} - {self.table}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
