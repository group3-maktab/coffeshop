import uuid
from core.models import BaseModel
from django.db import models


class Table(BaseModel):
    status_fields = [("R", "Reserved"), ("E", "Empty"), ("F", "Full"), ("T", "TakeAway")]

    number = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=status_fields, default='E')

    def __str__(self) -> str:
        return f'{self.number}'


class Reservation(BaseModel):
    status_fields = [("A", "Accept"), ("D", "Denied"), ("O", "On_Process")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL,
                              null=True, default=None)  # todo:ask????
    status = models.CharField(max_length=1, choices=status_fields, default='O')
    phone_number = models.CharField(max_length=11)
    number_of_persons = models.PositiveIntegerField()
    datetime = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.phone_number} | {self.datetime} | {self.status} | {self.table}'
