from django import template

register = template.Library()


@register.assignment_tag
def total_charge(cart):
    total = 0
    for item in cart:
        total += item.price
    return total
