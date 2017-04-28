from django import template

from Bikes import models, forms
from shopping_cart.models import Cart

register = template.Library()


@register.assignment_tag
def amount_items_in_cart(user):
    user_profile = models.Order.objects.get(name=user.username, email=user.email)
    cart = Cart.objects.filter(user=user_profile)
    amount = 0
    for item in cart:

        if item.quantity > 0:
            amount += item.quantity
    return amount


@register.assignment_tag
def customers(reservations):
    """ for superuser to see all reservations on one bike """
    user_list = {}
    for order in reservations:
        user = order.user_info
        if user not in user_list:
            user_list[user] = {
                order.order: {
                    'billings': {order.address: 1},
                    'cards': {order.payment: order.order.price},
                    'total': order.order.price,
                    'amount': 1
                }
            }
        else:
            if order.order in user_list[user]:
                if order.address not in user_list[user][order.order]['billings']:
                    user_list[user][order.order]['billings'][order.address] = 1
                else:
                    user_list[user][order.order]['billings'][order.address] += 1
                if order.payment not in user_list[user][order.order]['cards']:
                    user_list[user][order.order]['cards'][order.payment] = order.order.price
                else:
                    user_list[user][order.order]['cards'][order.payment] += order.order.price
                user_list[user][order.order]['total'] += order.order.price
                user_list[user][order.order]['amount'] += 1
            else:
                # add new part to dict
                user_list[user][order.order] = {
                    'billings': {order.address: 1},
                    'cards': {order.payment: order.order.price},
                    'total': order.order.price,
                    'amount': 1
                }
            # user_list[user].append(order)
    return user_list


@register.assignment_tag()
def get_bill_form(bill):
    """ returns a BillingForm with the instance of the bill """
    bill_form = forms.BillingForm(instance=bill)
    return bill_form


@register.assignment_tag()
def get_card_form(card):
    """ returns a CardForm with the instance of the card """
    card_form = forms.CardForm(instance=card)
    return card_form


@register.filter('preorders_needed')
def preorders_needed(bike):
    """ returns how much reservations needed till confirm the sale """
    left = bike.orders_needed - bike.orders
    return left


@register.assignment_tag
def order_link(user_name):
    """  """
    return models.Order.objects.get(name=user_name)


@register.assignment_tag
def bikes_available(type):
    """ returns if there is any bikes available for sale from that type."""
    bikes = models.Bikes.objects.filter(type=type)
    return bikes


@register.assignment_tag
def orders_by_bike(orders):
    """ returns all bikes reserved or bought by user  """
    bike_list = []
    for order in orders:
        bike = models.Bikes.objects.get(name=order.order)
        if bike not in bike_list:
            bike_list.append(bike)
    return bike_list


@register.assignment_tag
def orders_by_address(orders, user):
    """ returns all addresses previously used or added by the user """
    bike_list = {}
    for order in orders:
        try:
            bike = models.Billing.objects.get(address=order.address.address, user_info=user)
            if bike not in bike_list:
                bike_list[bike] = 1
            else:
                bike_list[bike] += 1
        except:
            pass
    return bike_list


@register.assignment_tag
def orders_by_card(orders, user):
    """ returns all Cards previously used or added by the user """
    bike_list = {}
    amount = {}
    for order in orders:
        price = order.order.price
        try:
            bike = models.Card.objects.get(number=order.payment.number, user_info=user)
            if bike not in bike_list:
                bike_list[bike] = price
                amount[bike] = 1
            else:
                amount[bike] += 1
                bike_list[bike] = price * amount[bike]
        except:
            pass
    return bike_list


@register.assignment_tag
def get_status(status):
    """ just user to assign 'status' to a variable """
    return status


@register.assignment_tag
def orders_by_customer_filter(orders, user):
    """ returns all orders (Preorders) of user """
    new_orders = []
    for order in orders:
        if order.user_info == user:
            new_orders.append(order)
    return new_orders


@register.assignment_tag
def reserved_by_customer(reservations):
    """ for superuser to see all reservations on one bike """
    user_list = {}
    for order in reservations:
        user = models.Order.objects.get(name=order.user_info.name, email=order.user_info.email)
        if user not in user_list:
            user_list[user] = 1
        else:
            user_list[user] += 1
    return user_list


@register.assignment_tag
def order_per_bike(bike, user, status):
    """ returns all orders (Preorders) of a posific bike and of a posific status and of the user """
    preorders = models.Preorders.objects.filter(user_info=user, order=bike, status=status)
    return preorders


@register.assignment_tag
def get_total_charge(orders, bike):
    """ get the total that person would be charged for items in Shopping cart """
    amount = 0
    for preorder in orders:
        amount += 1
    return amount * bike.price


@register.assignment_tag
def order_per_address(address, user, status):
    """ returns the amount of orders being send to an address """
    preorders = models.Preorders.objects.filter(user_info=user, address=address, status=status)
    amount = 0
    for preorder in preorders:
        amount += 1
    return amount
