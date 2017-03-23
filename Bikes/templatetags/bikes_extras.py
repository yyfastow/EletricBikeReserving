from django import template

from Bikes import models, forms

register = template.Library()

@register.assignment_tag()
def get_bill_form(bill):
    bill_form = forms.BillingForm(instance=bill)
    return bill_form


@register.assignment_tag()
def get_card_form(card):
    card_form = forms.CardForm(instance=card)
    return card_form


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
def orders_by_address(orders, user):
    bike_list = {}
    for order in orders:
        bike = models.Billing.objects.get(address=order.address.address, user_info=user)
        if bike not in bike_list:
            bike_list[bike] = 1
        else:
            bike_list[bike] += 1
    return bike_list


@register.assignment_tag
def orders_by_card(orders, user):
    bike_list = {}
    amount = {}
    for order in orders:
        price = order.order.price
        bike = models.Card.objects.get(number=order.payment.number, user_info=user)
        if bike not in bike_list:
            bike_list[bike] = price
            amount[bike] = 1
        else:
            amount[bike] += 1
            bike_list[bike] = price * amount[bike]
    return bike_list



@register.assignment_tag
def get_status(status):
    return status


@register.assignment_tag
def order_per_bike(bike, user, status):
    preorders = models.Preorders.objects.filter(user_info=user, order=bike, status=status)

    return preorders

@register.assignment_tag
def get_total_charge(orders, bike):
    amount = 0
    for preorder in orders:
        amount += 1
    return amount * bike.price


@register.assignment_tag
def order_per_address(address, user, status):
    preorders = models.Preorders.objects.filter(user_info=user, address=address, status=status)
    amount = 0
    for preorder in preorders:
        amount += 1
    return amount