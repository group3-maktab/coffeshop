from django.db import models
from django.db import models

# Create your models here.
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

    @property
    def is_subcategory(self):
        return self.parent is not None


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    off = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    @property
    def price_after_off(self):
        return self.price - (self.price * self.off / 100)
