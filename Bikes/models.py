from django.core.validators import RegexValidator
from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
from localflavor.us.models import USStateField, USZipCodeField


class BikeTypes(models.Model):
    type = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='images')

    def __str__(self):
        return self.type


class Bikes(models.Model):
    type = models.ForeignKey(BikeTypes)
    name = models.CharField(max_length=100)
    picture = models.ImageField()
    description = models.TextField()
    price = MoneyField(max_digits=7,
                       decimal_places=2,
                       default_currency='USD',
                       )
    orders_needed = models.IntegerField(default=5)
    orders = models.IntegerField(default=0)


    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('bikes:details', kwargs={
            'type_pk': self.type_id,
            'bike_pk': self.id
        })

    def __str__(self):
        return self.name


class Order(models.Model):
    total_charge = MoneyField(max_digits=7,
                       decimal_places=2,
                       default_currency='USD'
                       )
    # charged = models.FloatField(default=0)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone Number")
    phone = models.CharField(max_length=17, validators=[phone_regex])
    #state = USStateField()
    #city = models.CharField(max_length=25)
    #address = models.CharField(max_length=100)
    #zip = USZipCodeField()
    #number = models.IntegerField("Credit Card Number")
    #expiration = models.DateTimeField()
    #ccv_number = models.IntegerField("CCV Number")
                                    # validators=([MaxValueValidator(9999)]))

    # , widget = forms.TextInput(attrs={'size': '4'})

    def __str__(self):
        return self.name


class Billing(models.Model):
    DEFAULT_PK=1
    user_info = models.ForeignKey(Order, default=DEFAULT_PK)
    state = USStateField()
    city = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    zip = USZipCodeField()

    def __str__(self):
        return self.address


class Card(models.Model):
    DEFAULT_PK=1
    user_info = models.ForeignKey(Order, default=DEFAULT_PK)
    number = models.IntegerField("Credit Card Number")
    expiration = models.DateTimeField()
    ccv_number = models.IntegerField("CCV Number")
                                    # validators=([MaxValueValidator(9999)]))

    # , widget = forms.TextInput(attrs={'size': '4'})

    def __str__(self):
        str = "{}".format(self.number)
        return "****-****-****-{}".format(str[-4:])



class Preorders(models.Model):
    user_info = models.ForeignKey(Order)
    address = models.ForeignKey(Billing)
    payment = models.ForeignKey(Card)
    order = models.ForeignKey(Bikes)
    status = models.CharField(max_length=25, default="reserved")

    def __str__(self):
        return self.order.name


class Message(models.Model):
    user = models.ForeignKey(Order)
    message = models.TextField()

    def __str__(self):
        return "{}".format(self.id)