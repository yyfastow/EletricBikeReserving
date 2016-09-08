from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from Bikes import models, forms
from Bikes.models import Preorders


# All Bikes views
def bike_type_list(request):
    """ shows all types of bikes available """
    bike_types = models.BikeTypes.objects.all()
    return render(request,
                  'bikes/bike_types.html',
                  {'bike_types': bike_types})


class BikeView(ListView):
    context_object_name = "bike_types"
    model = models.BikeTypes


def bike_list(request, pk):
    """ shows all bikes in those categories"""
    types = models.BikeTypes.objects.get(pk=pk)
    bikes = models.Bikes.objects.filter(type=types)
    return render(request,
                  'bikes/bike_list.html',
                  {'types': types, 'bikes': bikes})


def bike_details(request, types_pk, bike_pk):
    """ show all bikes details"""
    bike = get_object_or_404(models.Bikes,
                             type_id=types_pk,
                             pk=bike_pk)
    more = bike.orders_needed - bike.orders
    return render(request,
                  'bikes/bikes_details.html',
                  {'bike': bike, 'more': more})


# Users Views
def message(request):
    """user could create a message to send as message to admin"""
    user = request.user
    order = ""
    if request.user.is_authenticated():
        if user.is_superuser:
            return HttpResponseRedirect(reverse('bikes:all_orders'))
        order = models.Order.objects.get(name=user.username, email=user.email)
    else:
        order = models.Order.objects.get(name="Anonymous")
    message = forms.MessageForm()
    if request.method == "POST":
        message = forms.MessageForm(request.POST)
        if message.is_valid():
            form = message.save(commit=False)
            form.user = order
            form.owner = "to"
            form.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'bikes/admin_messages.html', {'message': message})


@login_required
def users_orders(request):
    """show all orders from current user"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    preorders = models.Preorders.objects.filter(user_info=order, status="reserved")
    return render(request, 'bikes/user_orders.html', {'user': user, 'order': order, 'preorders': preorders})


@login_required
def users_orders_ready(request):
    """ show all orders from current user that are ready for shipping """
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    shipping = models.Preorders.objects.filter(user_info=order, status="shipping")
    shipped = models.Preorders.objects.filter(user_info=order, status="shipped")
    return render(request, 'bikes/orders_ready.html', {'user': user, 'order': order, 'shipping': shipping, 'shipped': shipped})


@login_required
def order_details(request, pk):
    """detailed order"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    bike = get_object_or_404(models.Bikes, pk=pk)
    user_profile = models.Order.objects.get(name=user.username, email=user.email)
    order = models.Preorders.objects.filter(user_info=user_profile, order=bike, status="reserved")
    return render(request,
                  'bikes/order_details.html',
                  {'user': user, 'orders': order, 'bike': bike, 'users': user_profile, 'status': 'shipped'})


@login_required
def ready_order_details(request, pk):
    """details or an order that is has anouf preorders to ship or status is "shipping" """
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    bike = get_object_or_404(models.Bikes, pk=pk)
    user_profile = models.Order.objects.get(name=user.username, email=user.email)
    order = models.Preorders.objects.filter(user_info=user_profile, order=bike, status="shipping")
    return render(request,
                  'bikes/send_details.html',
                  {'user': user, 'orders': order, 'bike': bike, 'users': user_profile, 'status': "shipping"})



@login_required
def sending_order_details(request, pk):
    """details or an order that is allready being shipped or status is "shipped"  """
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    bike = get_object_or_404(models.Bikes, pk=pk)
    user_profile = models.Order.objects.get(name=user.username, email=user.email)
    order = models.Preorders.objects.filter(user_info=user_profile, order=bike, status="shipped")
    return render(request,
                  'bikes/send_details.html',
                  {'user': user, 'orders': order, 'bike': bike, 'users': user_profile, 'status': "shipped"})


@login_required()
def edit_address(request, pk):
    """edits address of posidic order"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    bill = models.Billing.objects.get(pk=pk)
    if bill.user_info.email != user.email and bill.user_info != user.username:
        return users_orders(request)
    # bike = get_object_or_404(models.Bikes, type_id=types_pk, pk=bike_pk)
    form = forms.BillingForm(instance=bill)
    if request.method == "POST":
        form = forms.BillingForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "address edited!")
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/add.html', {'form': form})


@login_required()
def change_address(request, pk):
    """changes the card on a order"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.filter(name=user.username, email=user.email)
    form = forms.BillSelectionForm()
    form.fields['billing'].queryset = models.Billing.objects.filter(user_info=order)
    if request.method == "POST":
        form = forms.BillSelectionForm(request.POST)
        form.fields['billing'].queryset = models.Billing.objects.filter(user_info=order)
        if form.is_valid():
            preorder = models.Preorders.objects.get(pk=pk)
            # bike = models.Bikes.objects.get(name=preorder.order.name)
            billing = form.cleaned_data['billing']
            preorder.address = billing
            preorder.save()
            # messages.success(messages, "Card changed")
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/add.html', {'form': form})



@login_required()
def edit_card(request, pk):
    """edits card for order """
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Preorders.objects.get(pk=pk)

    if order.user_info.email != user.email and order.user_info != user.username:
        return users_orders(request)
    # bike = get_object_or_404(models.Bikes, type_id=types_pk, pk=bike_pk)
    form = forms.CardForm(instance=order.payment)
    if request.method == "POST":
        form = forms.CardForm(request.POST, instance=order.payment)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Credit card edited!")
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/add.html', {'form': form})


@login_required()
def change_card(request, pk):
    """changes the card on a order"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.filter(name=user.username, email=user.email)
    form = forms.CardSelectionForm()
    form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
    if request.method == "POST":
        form = forms.CardSelectionForm(request.POST)
        form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
        if form.is_valid():
            preorder = models.Preorders.objects.get(pk=pk)
            card = form.cleaned_data['card']
            preorder.payment = card
            preorder.save()
            # messages.success(messages, "Card changed")
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/add.html', {'form': form})


@login_required()
def edit_cards(request):
    """ edits all credit cards of user"""
    user = request.user
    order = models.Order.objects.get(name=user.username, email=user.email)
    card = models.Card.objects.filter(user_info=order)
    form = forms.CardFormSet(queryset=card)
    if request.method == 'POST':
        form = forms.CardFormSet(request.POST, queryset=card)
        if form.is_valid():
            cards = form.save(commit=False)
            for card in cards:
                card.user_info = order
                card.save()
            messages.success(request, "updated Credit card infomation!")
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/edit_cards.html', {'credit_cards': form})



@login_required
def edit_order(request):
    """form to edit information of user"""
    user = request.user
    order = models.Order.objects.get(name=user.username, email=user.email)
    form = forms.OrderForm(instance=order)
    billing = models.Billing.objects.filter(user_info=order)
    if request.method == 'POST':
        form = forms.OrderForm(request.POST, instance=order,)
        if form.is_valid() and email_name_unique(request,
                form.cleaned_data['name'], form.cleaned_data['email'], user):
            form.save()
            user.username = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, "updated Order!")
            # TODO: login automatically
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/edit_order.html', {'user': user,
                                                     'order': order,
                                                     'form': form,
                                                     'billings': billing,
                                                     })


def email_name_unique(request, name, email, user=None):
    """makes sure email and password is unique"""
    users_email = User.objects.filter(email=email)
    users_name = User.objects.filter(username=name)
    if users_email and user not in users_email:
        messages.success(request, "This email is allready used by another user")
        return False
    elif users_name and user not in users_name:
        messages.success(
            request,
            "This name is allready used by another costomer"
        )
        return False
    else:
        return True


@login_required()
def change_password(request):
    """form to change password"""
    user = request.user
    form = forms.PasswordForm()
    if request.method == 'POST':
        form = forms.PasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Changed Password!")
            # TODO: login automatically
            return HttpResponseRedirect(reverse('bikes:login'))
    return render(request, 'bikes/edit_order.html', {'user': user,
                                                          'form': form})


@login_required()
def cancel_order(request, pk):
    """ cancel an order"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    preorder = get_object_or_404(models.Preorders, pk=pk)
    order = models.Order.objects.get(name=user.username, email=user.email)
    bike = models.Bikes.objects.get(name=preorder.order)
    if request.method == 'POST' and preorder.status == 'reserved':
        preorder.delete()
        order.total_charge -= bike.price
        order.save()
        bike.orders -= 1
        bike.save()
        messages.add_message(request, messages.SUCCESS, "canceled order")
        return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/cancel_order.html', {'preorder': preorder, 'bike': bike})


# Ordering bikes
def order_bike(request, types_pk, bike_pk):
    """ makes form to order bike """
    bike = get_object_or_404(models.Bikes, pk=bike_pk)
    form = forms.OrderForm()
    password = forms.PasswordForm()
    billing = forms.BillingForm()
    card = forms.CardForm()
    amount = forms.AmountForm(request.GET, empty_permitted=True)
    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        password = forms.PasswordForm(request.POST)
        billing = forms.BillingForm(request.POST)
        card = forms.CardForm(request.POST)
        amount = forms.AmountForm(request.POST)
        if form.is_valid() and password.is_valid() and billing.is_valid() and card.is_valid() and amount.is_valid() and  email_name_unique(
                request, form.cleaned_data['name'], form.cleaned_data['email']):
            order = form.save(commit=False)
            order.total_charge = 0.00
            order.save()
            addr = billing.save(commit=False)
            addr.user_info = order
            addr.save()
            payment = card.save(commit=False)
            payment.user_info = order
            payment.save()

            for num in range(0, amount.cleaned_data['amount']):
                Preorders.objects.create(user_info=order,
                                         address=addr,
                                         payment=payment,
                                         order=bike)
                order.total_charge += bike.price
                order.save()
                bike.orders += 1
                bike.save()
                if bike.orders >= bike.orders_needed:
                    anought_orders(request, bike)
                else:
                    messages.add_message(request, messages.SUCCESS, "Your order is sent!")
            user = User.objects.create_user(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                password.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/order_form.html', {'form': form, 'billing': billing, 'card': card, 'bike': bike, 'password': password, 'amount': amount})


def anought_orders(request, bike):
    """ function that is triggered when anough bikes are ordered"""
    earlier_orders = models.Preorders.objects.filter(order=bike, status="reserved")
    for early in earlier_orders:
        user_in = early.user_info
        order = models.Order.objects.get(name=user_in.name, email=user_in.email)
        billing = early.address
        card = early.payment
        # changes status of the order to "shipping"
        early.status = "shipping"
        early.save()
        # sends mail to admin
        send_mail(
            "Order for {}".format(bike.name),
            """Bike: {}
            Name: {}
            Phone Number: {}
            Billing Address: {} {} {} {}
            Credit Card Number: {}
            expiration: {}
            CCV number: {}
            """.format(bike.name, user_in.name, user_in.phone, billing.address, billing.city,
                billing.state, billing.zip, card.number, card.expiration, card.ccv_number),
            '{} <{}>'.format(user_in.name, user_in.email),
            ['yoseffastow@gmail.com'],
        )
        # creats massage to show to user that item is ready to ship
        carded = "{}".format(card.number)
        models.Message.objects.create(
            user=order,
            message="""Order of bike {} is ready to be send to {} {} {} {}.
                    We will charge your credit card ****-{} shortly {} price and ship it as soon as possible
                    We will tell you when. """.format(bike.name, billing.address, billing.city,
                                                      billing.state, billing.zip, carded[-4:],
                                                      bike.price)
        )
        user = models.Order.objects.get(name=early.user_info.name)
        user.total_charge -= bike.price
        user.save()
    bike.orders = 0
    bike.save()
    messages.add_message(request, messages.SUCCESS, "You order is sent and ready for shipping")


@login_required
def order_another_bike(request, types_pk, bike_pk):
    """adds another order"""
    bike = get_object_or_404(models.Bikes, pk=bike_pk)
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    form = forms.SelectionForm()
    form.fields['billing'].queryset = models.Billing.objects.filter(user_info=order)
    form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
    amount = forms.AmountForm(request.POST, empty_permitted=True)
    if request.method == "POST":
        form = forms.SelectionForm(request.POST)
        form.fields['billing'].queryset = models.Billing.objects.filter(user_info=order)
        form.fields['card'].queryset = models.Card.objects.filter(user_info=order)
        if form.is_valid() and amount.is_valid():
            for num in range(0, amount.cleaned_data['amount']):
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
                    messages.add_message(request, messages.SUCCESS, "Your order is sent to {} with a card!".format(
                        form.cleaned_data['billing'],
                    ))
                else:
                    messages.add_message(request, messages.SUCCESS, "Your order is sent to {} with a card!".format(
                        form.cleaned_data['billing'],
                    ))
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/confirm_order.html', {'user': user,'bike': bike, 'form': form, 'amount': amount})


@login_required()
def add_address(request, types_pk, bike_pk):
    """ User could add another address """
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    # bike = get_object_or_404(models.Bikes, type_id=types_pk, pk=bike_pk)
    form = forms.BillingForm()
    if request.method == "POST":
        form = forms.BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.user_info = order
            billing.save()
            messages.add_message(request, messages.SUCCESS, "address added!")
            return HttpResponseRedirect(reverse('bikes:order_more', args=(types_pk, bike_pk)))
    return render(request, 'bikes/add.html', {'form': form})


@login_required()
def add_card(request, types_pk, bike_pk):
    """form to add a credit card"""
    user = request.user
    if user.is_superuser:
        return admin_orders(request)
    order = models.Order.objects.get(name=user.username, email=user.email)
    # bike = get_object_or_404(models.Bikes, type_id=types_pk, pk=bike_pk)
    form = forms.CardForm()
    if request.method == "POST":
        form = forms.CardForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.user_info = order
            billing.save()
            messages.add_message(request, messages.SUCCESS, "Credit card added!")
            return HttpResponseRedirect(reverse('bikes:order_more', args=(types_pk, bike_pk)))
    return render(request, 'bikes/add.html', {'form': form})


# Loggin in and out
def loginer(request):
    """Logins user"""
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "You are now login!")
                    return HttpResponseRedirect(reverse('bikes:type'))
                else:
                    messages.add_message(request, messages.ERROR, "This account has been disabled sorry!")
                    return HttpResponseRedirect(reverse('bikes:type'))
            else:
                messages.add_message(request, messages.ERROR, "Invalid Login!")
    return render(request, 'bikes/login.html', {'form': form})


def logout_view(request):
    """logs out user"""
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successfully!")
    return HttpResponseRedirect(reverse('bikes:type'))


# Admin views
@user_passes_test(lambda user: user.is_superuser)
def admin_orders(request):
    """admin could see all costomers"""
    orders = models.Order.objects.all()
    return render(request, 'bikes/all_orders.html', {'orders': orders})


@user_passes_test(lambda user: user.is_superuser)
def admin_user_preorders(request, pk):
    """admin could see all orders by person """
    order = models.Order.objects.get(pk=pk)
    preorders = models.Preorders.objects.filter(user_info=order)
    return render(request, 'bikes/admin_users_orders.html', {'preorders': preorders, 'order': order})


@user_passes_test(lambda user: user.is_superuser)
def admin_orders_bike(request, pk):
    """admin could see all orders by bike"""
    bike = get_object_or_404(models.Bikes, pk=pk)
    preorders = models.Preorders.objects.filter(order=bike)
    return render(request, 'bikes/orders_list.html', {'bike': bike, 'preorders': preorders})


@user_passes_test(lambda user: user.is_superuser)
def orders_ready_to_ship(request):
    """admin sees all items ready to ship"""
    preorders = models.Preorders.objects.filter(status="shipping")
    shipped = models.Preorders.objects.filter(status="shipped")
    return render(request, 'bikes/orders_shiping.html', {'preorders': preorders, 'shipped': shipped})


@user_passes_test(lambda user: user.is_superuser)
def admin_send_message(request, pk):
    """ form for admin to send a message to a costomer"""
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
    return render(request, 'bikes/admin_messages.html', {'message': message, 'order': order})


@user_passes_test(lambda user: user.is_superuser)
def shipping_order(request, pk):
    """ admin confirms that item is sent and marks it as shipped"""
    preorder = models.Preorders.objects.get(pk=pk)
    preorder.status = 'shipped'
    preorder.save()
    order = models.Order.objects.get(name=preorder.user_info.name)
    models.Message.objects.create(
        user=order,
        message="""Your card was charged and {} is being shipped to you it will come to you in the next month
                    Contact us about.
                """.format(preorder.order)
    )
    messages.add_message(request, messages.SUCCESS, "Marked as shipped")
    return HttpResponseRedirect(reverse('bikes:shipping'))

@user_passes_test(lambda user: user.is_superuser)
def recieved_order(request, pk):
    """ admin confirms that item is sent and marks it as shipped"""
    preorder = models.Preorders.objects.get(pk=pk)
    preorder.status = 'recieved'
    preorder.save()
    messages.add_message(request, messages.SUCCESS, "Marked as revieved")
    return HttpResponseRedirect(reverse('bikes:shipping'))
