from django.db import models
from djmoney.models.fields import MoneyField

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
    # TODO: want to use MondeyField to be mare accuret but it doesn't work. I inastalled it in pip
    price = MoneyField(max_digits=7,
                            decimal_places=2,
                            default_currency='USD'
                       )

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('bikes:details', kwargs={
            'type_pk': self.type_id,
            'bike_pk': self.id
        })

    def __str__(self):
        return self.name


"""class Orders(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    zip = models.IntegerField(max_length=5)"""

