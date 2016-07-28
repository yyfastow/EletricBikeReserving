from django import template

from Bikes.models import Bikes


register = template.Library()


@register.filter('preorders_needed')
def preorders_needed(bike):
    """ returns how much preorders are needed until """
    left = bike.orders_needed - bike.orders
    return left