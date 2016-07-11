
import moneyed
from djmoney.models.fields import MoneyField

from django.db import models

# Create your models here.


class BikeTypes(models.Model):
    type = models.CharField(max_length=100)
    picture = models.ImageField()

    def __str__(self):
        return self.type


class Bikes(models.Model):
    type = models.ForeignKey(BikeTypes)
    name = models.CharField(max_length=100)
    picture = models.ImageField()
    description = models.TextField()
    price = models.FloatField()
    # TODO: want to use MondeyField to be mare accuret but it doesn't work. I inastalled it in pip
    #price = MoneyField(max_digits=7,
    #                         decimal_places=2,
    #                        default_currenty='USD')

    def __str__(self):
        return self.name


"""class Orders(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    zip = models.IntegerField(max_length=5)"""

