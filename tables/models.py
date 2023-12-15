from django.db import models


class Table(models.Model):
    reservation = [("r", "reserved"), ("e", "empty"), ("f", "full")]
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=reservation)
