from django import template

from Bikes import models
from Bikes.models import Bikes

register = template.Library()


@register.filter('preorders_needed')
def preorders_needed(bike):
    """ returns how much preorders are needed until """
    left = bike.orders_needed - bike.orders
    return left


@register.assignment_tag
def order_link(user_name):
    return models.Order.objects.get(name=user_name)


@register.assignment_tag
def bikes_available(type):
    bikes = models.Bikes.objects.filter(type=type)
    return bikes


@register.assignment_tag
def orders_by_bike(orders):
    bike_list = []
    for order in orders:
        bike = models.Bikes.objects.get(name=order.order)
        if bike not in bike_list:
            bike_list.append(bike)
    return bike_list



@register.assignment_tag
def orders_by_address(orders):
    bike_list = []
    for order in orders:
        bike = models.Billing.objects.get(address=order.address.address)
        if bike not in bike_list:
            bike_list.append(bike)
    return bike_list


@register.assignment_tag
def order_per_bike(bike, user, status):
    preorders = models.Preorders.objects.filter(user_info=user, order=bike, status=status)
    amount = 0
    for preorder in preorders:
        amount += 1
    return amount


@register.assignment_tag
def order_per_address(address, user, status):
    preorders = models.Preorders.objects.filter(user_info=user, address=address, status=status)
    amount = 0
    for preorder in preorders:
        amount += 1
    return amount