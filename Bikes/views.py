from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms import forms
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView

from Bikes import models, forms
from Bikes.models import Preorders

# All Bikes views
from shopping_cart.models import Cart
from shopping_cart.views import add_to_cart, show_cart


def email_name_unique(request, name, email, user=None):
    """makes sure email and password are unique"""
    users_email = User.objects.filter(email=email)
    users_name = User.objects.filter(username=name)
    if users_email and user not in users_email:
        messages.error(request, "This email is already used by another user")
        return False
    elif users_name and user not in users_name:
        messages.error(
            request,
            "This name is already used by another costumer"
        )
        return False
    else:
        return True


# bikes
def bike_type_list(request):
    """ shows all types of bikes available """
    bike_types = models.BikeTypes.objects.all()
    return render(request, 'bikes/bike_types.html', {'bike_types': bike_types})


def bike_list(request, pk):
    """ shows all bikes in those categories"""
    types = models.BikeTypes.objects.get(pk=pk)
    bikes = models.Bikes.objects.filter(type=types)
    return render(request,
                  'bikes/bike_list.html',
                  {'types': types, 'bikes': bikes})


def bike_details(request, types_pk, bike_pk):
    """ show all bikes details. As a costumer there is a button to add bike to cart. If you are a new customer there's a
    form on bottom to make a new account before adding to cart. For admin there's a list of all orders on that bike."""
    bike = get_object_or_404(models.Bikes, type_id=types_pk, pk=bike_pk)
    more = bike.orders_needed - bike.orders
    form = forms.OrderForm(request.POST or None)
    password = forms.PasswordForm(request.POST or None)
    reservations = ""
    amount_form = ""
    shipping = ""
    shipped = ""
    if request.user.is_superuser:
        reservations = models.Preorders.objects.filter(status="reserved", order=bike)
        shipping = models.Preorders.objects.filter(status="shipping", order=bike)
        shipped = models.Preorders.objects.filter(status="shipped", order=bike)
    else:
        amount_form = forms.AmountForm(request.POST, empty_permitted=True)
        if form.is_valid() and password.is_valid() and amount_form.is_valid() and email_name_unique(
                request, form.cleaned_data['name'], form.cleaned_data['email']):
            amount = request.POST.get('amount')
            order = form.save(commit=False)
            order.total_charge = 0.00
            order.save()
            user = User.objects.create_user(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                password.cleaned_data['password']
            )
            login(request, user)
            print(amount)
            return add_to_cart(request, bike_pk, amount)
    return render(request, 'bikes/bikes_details.html', {'bike': bike, 'more': more, 'form': form, 'password': password,
                                                        'reservations': reservations, 'shipping': shipping,
                                                        'shipped': shipped})


# order's
@login_required
def users_orders(request):
    """show all orders from current user"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    preorders = models.Preorders.objects.filter(user_info=order, status="reserved")
    shipping = models.Preorders.objects.filter(user_info=order, status="shipping")
    shipped = models.Preorders.objects.filter(user_info=order, status="shipped")
    # if len(preorders) < 1 and len(shipping) < 1 and len(shipped) < 1:
    if not preorders and not shipping and not shipped:
        messages.warning(request, "You have no items reserved or shipped. Here is your shopping cart!")
        return show_cart(request)
    return render(request, 'bikes/user_orders.html', {'user': user, 'order': order, 'preorders': preorders, 'shipping': shipping, 'shipped': shipped})


# @login_required
# def users_orders_ready(request):
#     """ show all orders from current user that are ready for shipping """
#     user = request.user
#     if user.is_superuser:
#         return admin_orders(request)
#     order = models.Order.objects.get(name=user.username, email=user.email)
#     shipping = models.Preorders.objects.filter(user_info=order, status="shipping")
#     shipped = models.Preorders.objects.filter(user_info=order, status="shipped")
#     return render(request, 'bikes/orders_ready.html',
#                   {'user': user, 'order': order, 'shipping': shipping, 'shipped': shipped})


@login_required
def order_details(request, pk):
    """ Details of order on a pacific bike.
    You have the option to change address of shipping and card here too"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    bike = get_object_or_404(models.Bikes, pk=pk)
    user_profile = models.Order.objects.get(name=user.username, email=user.email)
    order = models.Preorders.objects.filter(user_info=user_profile, order=bike, status="reserved")
    print(order)
    print(len(order))
    if len(order) == 0:
        print("You made no orders")
        return users_orders(request)
    bills = models.Billing.objects.filter(user_info=user_profile)
    credit_cards = models.Card.objects.filter(user_info=user_profile)
    return render(request, 'bikes/order_details.html',
                  {'user': user, 'orders': order, 'bills': bills, 'credit_cards': credit_cards, 'bike': bike,
                   'users': user_profile, 'status': 'shipped'})



# @login_required
# def ready_order_details(request, pk):
#     """details or an order that is has anouf preorders to ship or status is "shipping" """
#     user = request.user
#     if user.is_superuser:
#         return admin_orders(request)
#     bike = get_object_or_404(models.Bikes, pk=pk)
#     user_profile = models.Order.objects.get(name=user.username, email=user.email)
#     order = models.Preorders.objects.filter(user_info=user_profile, order=bike, status="shipping")
#     return render(request,
#                   'bikes/send_details.html',
#                   {'user': user, 'orders': order, 'bike': bike, 'users': user_profile, 'status': "shipping"})


# @login_required
# def sending_order_details(request, pk):
#     """details or an order that is allready being shipped or status is "shipped"  """
#     user = request.user
#     if user.is_superuser:
#         return admin_orders(request)
#     bike = get_object_or_404(models.Bikes, pk=pk)
#     user_profile = models.Order.objects.get(name=user.username, email=user.email)
#     order = models.Preorders.objects.filter(user_info=user_profile, order=bike, status="shipped")
#     return render(request,
#                   'bikes/send_details.html',
#                   {'user': user, 'orders': order, 'bike': bike, 'users': user_profile, 'status': "shipped"})


# change personal info
# address


@login_required()
def add_address(request):
    """ User could add another address. """
    user = request.user
    next = request.GET.get('next')
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    form = forms.BillingForm()
    if request.method == "POST":
        form = forms.BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.user_info = order
            billing.save()
            new_text = billing.address + ", " + billing.city + ", " + billing.state
            if request.is_ajax():
                return JsonResponse({
                    'pk': billing.pk,
                    'new_text': new_text
                })
            else:
                messages.add_message(request, messages.SUCCESS, "address added!")
                if next:
                    return redirect(next)
                return HttpResponseRedirect(reverse('bikes:user'))

    return render(request, 'bikes/add.html', {'form': form})


@login_required()
def change_address(request):
    """changes the address on a order."""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.filter(name=user.username, email=user.email)
    orders = request.POST.get("orders")
    try:
        orders = orders.split(" ")
    except AttributeError:
        return HttpResponseRedirect(reverse('bikes:edit'))
    del orders[-1]
    print(orders)
    for item in orders:
        selection = request.POST.get("billing"+item)
        try:
            address = models.Billing.objects.get(pk=selection, user_info=order)
            preorder = models.Preorders.objects.get(pk=item, user_info=order)
            preorder.address = address
            preorder.save()
        except ValueError:
            pass
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required()
def edit_address(request):
    """edits address of pacific order"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    pk = request.POST.get('pk')
    if not pk:
        return HttpResponseRedirect(reverse('bikes:edit'))
    bill = models.Billing.objects.get(pk=pk)
    if bill.user_info.email != user.email and bill.user_info != user.username:
        return users_orders(request)
    form = forms.BillingForm(instance=bill)
    if request.method == "POST":
        form = forms.BillingForm(request.POST, instance=bill)
        if form.is_valid():
            bill = form.save(commit=False)
            text = bill.address + ", " + bill.city + ", " + bill.state + ", " + bill.zip
            bill.save()
            if request.is_ajax():
                return JsonResponse({
                    'text': text
                })
            else:
                messages.add_message(request, messages.SUCCESS, "address edited!")
            return HttpResponseRedirect(reverse('bikes:edit'))
    return render(request, 'bikes/add.html', {'form': form})


# credit card
@login_required()
def edit_card(request):
    """edits card for order """
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    or_user = models.Order.objects.get(name=user.username, email=user.email)
    pk = request.POST.get('pk')
    if not pk:
        return HttpResponseRedirect(reverse('bikes:edit'))
    card = models.Card.objects.get(pk=pk, user_info=or_user)
    print(pk)
    form = forms.CardForm(instance=card)
    if request.method == "POST":
        form = forms.CardForm(request.POST, instance=card)
        if form.is_valid():
            cards = form.save(commit=False)
            credit_card = "{}".format(cards.number)
            text = "****-****-****-{}".format(credit_card[-4:])
            cards.save()
            if request.is_ajax():
                return JsonResponse({'card': text, 'error': 'good'})
            else:
                messages.add_message(request, messages.SUCCESS, "Credit card edited!")
                return HttpResponseRedirect(reverse('bikes:edit'))
        else:
            expiration = form.cleaned_data['expiration']
            if request.is_ajax():
                err = "Card is invalid. Use another credit card or make sure you put in the data correctly."
                if expiration <= datetime.now().date():
                    err = "Your card is expired!"
                return JsonResponse({'error': err})
            else:
                messages.error(request, "Didn't edit!")
    return render(request, 'bikes/add.html', {'form': form})


def change_card(request):
    """changes the card on a order"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.filter(name=user.username, email=user.email)
    orders = request.POST.get("orders")
    try:
        orders = orders.split(" ")
    except AttributeError:
        return HttpResponseRedirect(reverse('bikes:edit'))
    del orders[-1]
    print(orders)
    for item in orders:
        selection = request.POST.get("card"+item)
        try:
            card = models.Card.objects.get(pk=selection)
            preorder = models.Preorders.objects.get(pk=item)
            preorder.payment = card
            preorder.save()
        except ValueError:
            pass
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# @login_required()
# def change_card(request, pk):
#     """changes the card on a order"""
#     user = request.user
#     if user.is_superuser:
#         return admin_orders(request)
#     order = models.Order.objects.filter(name=user.username, email=user.email)
#     form = forms.CardSelectionForm()
#     form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
#     if request.method == "POST":
#         form = forms.CardSelectionForm(request.POST)
#         form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
#         if form.is_valid():
#             preorder = models.Preorders.objects.get(pk=pk)
#             card = form.cleaned_data['card']
#             preorder.payment = card
#             preorder.save()
#             # messages.success(messages, "Card changed")
#             return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
#     return render(request, 'bikes/add.html', {'form': form})

#
# @login_required()
# def edit_cards(request):
#     """ edits all credit cards of user"""
#     user = request.user
#     order = models.Order.objects.get(name=user.username, email=user.email)
#     card = models.Card.objects.filter(user_info=order)
#     card_form = forms.CardFormSet(request.POST, queryset=card)
#     if card_form.is_valid():
#         cards = card_form.save(commit=False)
#         for card in cards:
#             card.user_info = order
#             card.save()
#         messages.success(request, "updated Credit card information!")
#     else:
#         messages.error(request, "Info is not updated")
#     return HttpResponseRedirect(reverse('bikes:edit'))


@login_required()
def add_card(request):
    """form to add a credit card"""
    user = request.user
    next = request.GET.get('next')
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    form = forms.CardForm()
    if request.method == "POST":
        form = forms.CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user_info = order
            card.save()
            if request.is_ajax():
                return JsonResponse({
                    'pk': card.pk,
                    'new_text': card.number
                })
            else:
                messages.add_message(request, messages.SUCCESS, "Credit card added!")
                if next:
                    return redirect(next)
                return HttpResponseRedirect(reverse('bikes:checkout'))
        else:
            if request.is_ajax():
                err = "Card is invalid. Use another credit card or make sure you put in the data correctly."
                if form.cleaned_data['expiration'] <= datetime.now().date():
                    err = 'Your card has expired.'
                return JsonResponse({
                    'error': err
                })
    return render(request, 'bikes/add.html', {'form': form})


# edit order
@login_required
def edit_order(request):
    """form to edit information of user"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    form = forms.EditInfoForm(instance=order)
    billing = models.Billing.objects.filter(user_info=order)
    card = models.Card.objects.filter(user_info=order)
    # card_form = forms.CardFormSet(queryset=card)
    if request.method == 'POST':
        form = forms.EditInfoForm(request.POST, instance=order)
        # card_form = forms.CardFormSet(request.POST, queryset=card)
        if form.is_valid() and email_name_unique(request, form.cleaned_data['name'],
                                                 form.cleaned_data['email'], user):
            form.save()
            user.username = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            messages.success(request, "updated Info!")
            password = form.cleaned_data['password']
            if password and password != '':
                user.set_password(form.cleaned_data['password'])
                messages.success(request, "Changed Password!")
            user.save()
            new_user_info = authenticate(
                username=form.cleaned_data['name'],
                email=form.cleaned_data['email']
            )
            login(request, new_user_info)
            return HttpResponseRedirect(reverse('bikes:edit'))
    return render(request, 'bikes/edit_order.html', {'user': user, 'order': order, 'form': form,
                                                     # 'card_form': card_form,
                                                     'billings': billing, 'cards': card})


# change password not needed anymore
# @login_required()
# def change_password(request):
#     """form to change password"""
#     user = request.user
#     form = forms.PasswordForm()
#     if request.method == 'POST':
#         form = forms.PasswordForm(request.POST)
#         if form.is_valid():
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             messages.success(request, "Changed Password!")
#             return HttpResponseRedirect(reverse('bikes:login'))
#     return render(request, 'bikes/edit_order.html', {'user': user,
#                                                      'form': form})


# Ordering bikes
# def order_bike(request, types_pk, bike_pk):
#     """ Makes form to order bike. """
#     bike = get_object_or_404(models.Bikes, pk=bike_pk)
#     form = forms.OrderForm()
#     password = forms.PasswordForm()
#     billing = forms.BillingForm()
#     card = forms.CardForm()
#     amount = forms.AmountForm(request.GET, empty_permitted=True)
#     if request.method == "POST":
#         form = forms.OrderForm(request.POST)
#         password = forms.PasswordForm(request.POST)
#         billing = forms.BillingForm(request.POST)
#         card = forms.CardForm(request.POST)
#         amount = forms.AmountForm(request.POST)
#         if (form.is_valid() and password.is_valid() and billing.is_valid() and
#                 card.is_valid() and amount.is_valid() and email_name_unique(
#                 request, form.cleaned_data['name'], form.cleaned_data['email'])
#             ):
#             order = form.save(commit=False)
#             order.total_charge = 0.00
#             order.save()
#             addr = billing.save(commit=False)
#             addr.user_info = order
#             addr.save()
#             payment = card.save(commit=False)
#             payment.user_info = order
#             payment.save()
#
#             for num in range(0, amount.cleaned_data['amount']):
#                 Preorders.objects.create(user_info=order,
#                                          address=addr,
#                                          payment=payment,
#                                          order=bike)
#                 order.total_charge += bike.price
#                 order.save()
#                 bike.orders += 1
#                 bike.save()
#                 if bike.orders >= bike.orders_needed:
#                     anought_orders(request, bike)
#                 else:
#                     messages.add_message(request, messages.SUCCESS, "Your order is sent!")
#             # user = User.objects.create_user(
#             #     form.cleaned_data['name'],
#             #     form.cleaned_data['email'],
#             #     password.cleaned_data['password']
#             # )
#             # login(request, user)
#             return HttpResponseRedirect(reverse('bikes:user'))
#     return render(request, 'bikes/order_form.html',
#                   {'form': form, 'billing': billing, 'card': card, 'bike': bike, 'password': password,
#                    'amount': amount})


def anought_orders(request, bike):
    """ function that is triggered when anought bikes are ordered. marks all bikes that status as reserved to shipping.
    """
    earlier_orders = models.Preorders.objects.filter(order=bike, status="reserved")

    for early in earlier_orders:
        user_in = early.user_info
        order = models.Order.objects.get(name=user_in.name, email=user_in.email)
        billing = early.address
        card = early.payment
        # changes status of the order to "shipping"
        early.status = "shipping"
        early.save()
        user_in.total_charge -= bike.price
        user_in.save()
        # sends mail to admin
        """send_mail(
            "Order for {}".format(bike.name),
            ""Bike: {}
            Name: {}
            Phone Number: {}
            Billing Address: {} {} {} {}
            Credit Card Number: {}
            expiration: {}
            CCV number: {}
            "".format(bike.name, user_in.name, user_in.phone, billing.address, billing.city,
                       billing.state, billing.zip, card.number, card.expiration, card.ccv_number),
            '{} <{}>'.format(user_in.name, user_in.email),
            ['yoseffastow@gmail.com'],
        )"""
        nu = """Your order on {} is ready to shipped. We will ship it to {} and will charge credit card ending with
        {} {}!""".format(bike.name, early.address, early.payment.number, bike.price)
        models.Message.objects.create(
            user=order,
            message=nu
        )


    bike.orders = 0
    bike.save()



    """ user_list = {}
    for order in earlier_orders:
        user = order.user_info
        if user not in user_list:
            user_list[user] = {
                'billings': {order.address: 1},
                'cards': {order.payment: order.order.price},
                'total': order.order.price,
                'amount': 1
            }
        else:
            if order.address not in user_list[user]['billings']:
                user_list[user]['billings'][order.address] = 1
            else:
                user_list[user]['billings'][order.address] += 1
            if order.payment not in user_list[user]['cards']:
                user_list[user]['cards'][order.payment] = order.order.price
            else:
                user_list[user]['cards'][order.payment] += order.order.price
            user_list[user]['total'] += order.order.price
            user_list[user]['amount'] += 1

    for user, ord in enumerate(user_list):

        # creates massage to show to user that item is ready to ship
        # carded = "{}".format(card.number)
        nu = "Your reservation on bike {} is ready to be shipped.".format(bike.name)
        for key, value in enumerate(ord['billings']):
            nu += "We will ship {} to {}.".format(value, key)
        for key, value in enumerate(ord['cards']):
            nu += "we will charge {} {}.".format(value, key)
        models.Message.objects.create(
            user=order,
            message=nu
        )
        # user = models.Order.objects.get(name=early.user_info.name)"""
    messages.add_message(request, messages.SUCCESS, "You order is sent and ready for shipping")


@login_required()
def cancel_order(request):
    """ cancel an order. """
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    pk = request.POST.get('pk')
    if not pk:
        return HttpResponseRedirect(reverse('bikes:edit'))
    order = models.Order.objects.get(name=user.username, email=user.email)
    preorder = models.Preorders.objects.get(pk=pk, status="reserved", user_info=order)
    bike = models.Bikes.objects.get(name=preorder.order)
    preorder.delete()
    order.total_charge -= bike.price
    order.save()
    bike.orders -= 1
    bike.save()
    if request.is_ajax():
        new_data = models.Preorders.objects.filter(order=bike, user_info=order, status="reserved")
        length = len(new_data)
        return JsonResponse({
            'length': length
        })
    else:
        messages.add_message(request, messages.SUCCESS, "canceled order")
    return HttpResponseRedirect(reverse('bikes:user'))


@login_required()
def cancel_all_orders(request):
    """ cancel an order of a pacific bike"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    pk = request.POST.get('pk')
    if not pk:
        return HttpResponseRedirect(reverse('bikes:edit'))
    order = models.Order.objects.get(name=user.username, email=user.email)
    bike = models.Bikes.objects.get(pk=pk)
    preorders = models.Preorders.objects.filter(user_info=order, order=bike, status="reserved")
    for preorder in preorders:
        preorder.delete()
        order.total_charge -= bike.price
        order.save()
        bike.orders -= 1
        bike.save()
    messages.add_message(request, messages.SUCCESS, "canceled order")
    return HttpResponseRedirect(reverse('bikes:user'))


@login_required()
def first_checkout(request):
    """ order for the first time """
    user = get_object_or_404(models.Order, name=request.user.username)
    cart = Cart.objects.filter(user=user)
    if not cart:
        messages.error(request, "You cart is empty you can't preceded to checkout!")
        raise Http404
    billing_form = forms.BillingForm(request.POST or None)
    card_form = forms.CardForm(request.POST or None)
    if billing_form.is_valid() and card_form.is_valid():
        address = billing_form.save(commit=False)
        address.user_info = user
        address.save()
        payment = card_form.save(commit=False)
        payment.user_info = user
        payment.save()
        for item in cart:
            if item.user != user:
                continue
            bike = models.Bikes.objects.get(name=item.bike.name)
            for num in range(0, item.quantity):
                Preorders.objects.create(user_info=user,
                                         address=address,
                                         payment=payment,
                                         order=bike)
                user.total_charge += bike.price
                user.save()
                bike.orders += 1
                bike.save()
                if bike.orders >= bike.orders_needed:
                    anought_orders(request, bike)
                item.delete(keep_parents=True)
        messages.add_message(request, messages.SUCCESS, "Your order is sent!")
        return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/order_form.html', {
        'cart': cart,
        'order': user,
        'billing': billing_form,
        'card': card_form
    })


@login_required
def checkout(request):
    """adds another order"""
    if request.user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=request.user.username)
    cart = Cart.objects.filter(user=order)
    if not cart:
        messages.error(request, "You cart is empty you cant preceded to checkout!")
        return HttpResponseRedirect(reverse('bikes:type'))
    billing = models.Billing.objects.filter(user_info=order)
    card = models.Card.objects.filter(user_info=order)
    if not billing or not cart:
        return HttpResponseRedirect(reverse('bikes:first_checkout'))
    form = forms.SelectionForm(request.POST or None)
    form.fields['billing'].queryset = billing
    form.fields['card'].queryset = card
    add_address_form = forms.BillingForm()
    add_card_form = forms.CardForm()
    if form.is_valid():
        for item in cart:
            bike = models.Bikes.objects.get(pk=item.bike_id)
            for num in range(0, item.quantity):
                order.total_charge += bike.price
                order.save()
                Preorders.objects.create(user_info=order,
                                         address=form.cleaned_data['billing'],
                                         payment=form.cleaned_data['card'],
                                         order=bike)
                bike.orders += 1
                bike.save()
                if bike.orders >= bike.orders_needed:
                    anought_orders(request, bike)
            item.delete(keep_parents=True)
        messages.success(request,"""Your order is reserved! We will tell you when we are ready to ship. You could
            cancel anytime before there anought order's to ship and we won't charge you until we are ready to ship.
        """)
        return HttpResponseRedirect(reverse('bikes:user'))
    elif request.method == "POST":
        messages.error(request, "Form is not valid try again")
    user = request.user
    return render(request, 'bikes/confirm_order.html', {'cart': cart, 'user': user, 'form': form,  'add_address': add_address_form,
                                                        'add_card': add_card_form, 'addresses': billing, 'cards': card})


# @login_required
# def order_another_bike(request, types_pk, bike_pk):
#     """adds another order"""
#     bike = get_object_or_404(models.Bikes, pk=bike_pk)
#     user = request.user
#     if user.is_superuser:
#         return admin_orders(request)
#     order = models.Order.objects.get(name=user.username, email=user.email)
#     form = forms.SelectionForm()
#     form.fields['billing'].queryset = models.Billing.objects.filter(user_info=order)
#     form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
#     amount = forms.AmountForm(request.POST, empty_permitted=True)
#     if request.method == "POST":
#         form = forms.SelectionForm(request.POST)
#         form.fields['billing'].queryset = models.Billing.objects.filter(user_info=order)
#         form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
#         if form.is_valid() and amount.is_valid():
#             for num in range(0, amount.cleaned_data['amount']):
#                 order.total_charge += bike.price
#                 order.save()
#                 Preorders.objects.create(user_info=order,
#                                          address=form.cleaned_data['billing'],
#                                          payment=form.cleaned_data['card'],
#                                          order=bike)
#                 bike.orders += 1
#                 bike.save()
#                 if bike.orders >= bike.orders_needed:
#                     anought_orders(request, bike)
#                     messages.add_message(request, messages.SUCCESS, "Your order is sent to {} with a card!".format(
#                         form.cleaned_data['billing'],
#                     ))
#                 else:
#                     messages.add_message(request, messages.SUCCESS, "Your order is sent to {} with a card!".format(
#                         form.cleaned_data['billing'],
#                     ))
#             return HttpResponseRedirect(reverse('bikes:user'))
#     return render(request, 'bikes/confirm_order.html', {'user': user, 'bike': bike, 'form': form, 'amount': amount})


# Admin views
@login_required()
def change_reservation_amount(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    try:
        pk = request.POST.get('pk')
        amount = int(request.POST.get('amount'))
    except TypeError:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    bike = models.Bikes.objects.get(pk=pk)
    if amount > 0:
        bike.orders_needed = amount
        bike.save()
        if amount <= bike.orders:
            anought_orders(request, bike)
            if amount < bike.orders:
                messages.warning(
                    request,
                    "They are more reservations than orders. To be fair we will marked shipping all {} reservations!".format(bike.orders)
                )
            else:
                messages.success(request, "Objects marked as shipped")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required()
def admin_orders(request):
    """admin could see all costumers"""
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    orders = models.Order.objects.all()
    return render(request, 'bikes/all_orders.html', {'orders': orders})


@login_required()
def admin_user_preorders(request, pk):
    """admin could see all orders by person """
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    order = get_object_or_404(models.Order, pk=pk)
    reserved = models.Preorders.objects.filter(user_info=order, status="reserved")
    shipping = models.Preorders.objects.filter(user_info=order, status="shipping")
    shipped = models.Preorders.objects.filter(user_info=order, status="shipped")
    return render(request, 'bikes/admin_users_orders.html', {'reservations': reserved, 'shipped': shipped,
                                                             'shipping': shipping, 'order': order})


# @user_passes_test(lambda user: user.is_superuser)
# def admin_orders_bike(request, pk):
#     """admin could see all orders by bike"""
#     bike = get_object_or_404(models.Bikes, pk=pk)
#     preorders = models.Preorders.objects.filter(order=bike)
#     return render(request, 'bikes/templatetags/orders_list.html', {'bike': bike, 'preorders': preorders})


@login_required()
def orders_ready_to_ship(request):
    """admin sees all items ready to ship"""
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    preorders = models.Preorders.objects.filter(status="shipping")
    shipped = models.Preorders.objects.filter(status="shipped")
    return render(request, 'bikes/orders_shiping.html', {'preorders': preorders, 'shipped': shipped})


@login_required()
def admin_send_message(request):
    """ form for admin to send a message to a costumer"""
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    pk = request.POST.get('pk')
    order = get_object_or_404(models.Order, pk=pk)
    message = forms.MessageForm()
    if request.method == "POST":
        message = forms.MessageForm(request.POST)
        if message.is_valid():
            form = message.save(commit=False)
            form.user = order
            form.save()
            messages.add_message(request, messages.SUCCESS, "message sent!")
            return HttpResponseRedirect(reverse('bikes:all_orders'))
        else:
            messages.error(request, "Message not sent")
    return render(request, 'admin_messages.html', {'message': message, 'order': order})


@login_required()
def shipping_order(request):
    """ admin confirms that item is sent and marks it as shipped"""
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    address = get_object_or_404(models.Billing, pk=request.POST.get('address'))
    user = models.Order.objects.get(pk=request.POST.get('user'))
    bike = models.Bikes.objects.get(pk=request.POST.get('bike'))
    preorders = models.Preorders.objects.filter(user_info=user, address=address, status="shipping",order=bike)
    amount = 0
    for preorder in preorders:
        preorder.status = 'shipped'
        preorder.save()
        amount += 1
    models.Message.objects.create(
        user=user,
        message="""We just shipped {} {} to {}. It should come in should come some time next week
                    Contact us about.
                """.format(amount, bike, address)
    )
    if request.is_ajax():
        bikes = False
        users = False
        remaining_user = models.Preorders.objects.filter(user_info=user, status="shipping").exclude(
            order=bike
        )
        remaining_bikes = models.Preorders.objects.filter(user_info=user, status="shipping", order=bike).exclude(
            address=address
        )
        cards_dict = {}
        if len(remaining_user) > 0:
            users = True
        if len(remaining_bikes) > 0:
            bikes = True
            for n in remaining_bikes:
                card = "{}".format(n.payment.pk)
                if card in cards_dict.keys():
                    cards_dict[card] += bike.price
                else:
                    cards_dict[card] = bike.price
            for pk, price in cards_dict.items():
                cards_dict[pk] = "{}".format(price)
        return JsonResponse({
            'users': users,
            'bikes': bikes,
            'cards': cards_dict
        })
    else:
        messages.add_message(request, messages.SUCCESS, "Marked as shipped")
    return HttpResponseRedirect(reverse('bikes:type'))


@login_required()
def recieved_order(request, pk):
    """ admin confirms that item is sent and marks it as received"""
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    preorder = get_object_or_404(models.Preorders, pk=pk)
    preorder.status = 'received'
    preorder.save()
    messages.add_message(request, messages.SUCCESS, "Marked as received")
    return HttpResponseRedirect(reverse('bikes:admin_shipping'))
