from django.db import models

# Create your models here.
from djmoney.models.fields import MoneyField

from Bikes.models import Order, Bikes


class Cart(models.Model):
    user = models.ForeignKey(Order)
    bike = models.ForeignKey(Bikes)
    quantity = models.PositiveIntegerField(default=1)
    price = MoneyField(max_digits=7,
                       decimal_places=2,
                       default_currency='USD',
                       )

    def __str__(self):
        return self.bike.name
