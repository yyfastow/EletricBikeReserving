from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from Bikes import models, forms
from Bikes.models import Preorders


def bike_type_list(request):
    """ shows all types of bikes available """
    bike_types = models.BikeTypes.objects.all()
    return render(request,
                  'bikes/bike_types.html',
                  {'bike_types': bike_types})


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
    return render(request,
                  'bikes/bikes_details.html',
                  {'bike': bike})


@login_required
def edit_order(request, pk):
    user = request.user
    order = get_object_or_404(models.Order, pk=pk)
    if order.email != user.email:
        return users_orders(request)
    form = forms.OrderForm(instance=order)
    if request.method == 'POST':
        form = forms.OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            messages.success(request, "updated Order!")
            return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/order_form.html', {'order': order})


def order_bike(request, types_pk, bike_pk):
    """ makes form to order bike """
    bike = get_object_or_404(models.Bikes, pk=bike_pk)
    form = forms.OrderForm()
    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_charge = bike.price
            order.save()
            Preorders.objects.create(user_info=order, order=bike)
            bike.orders += 1
            bike.save()
            user = User.objects.create_user(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            """send_mail(
                "Order for {}".format(bike.name),
                ""Bike: {}
                Name: {name}
                Phone Number: {phone}
                Billing Address: {address} {city} {state} {zip}
                    expiration: {expiration}
                    CCV number: {ccv_number}
                "".format(bike.name, **form.cleaned_data),
                '{name} <{email}>'.format(**form.cleaned_data),
                ['yoseffastow@gmail.com'],
            )"""
            messages.add_message(request, messages.SUCCESS, "Your order is sent!")
            return HttpResponseRedirect(reverse('bikes:login'))
    return render(request, 'bikes/order_form.html', {'form': form, 'bike': bike})


@login_required
def order_another_bike(request, types_pk, bike_pk):
    """adds another order"""
    bike = get_object_or_404(models.Bikes, pk=bike_pk)
    if request.method == "POST":
        user = request.user
        order = models.Order.objects.get(name=user.username, email=user.email)
        order.total_charge += bike.price
        order.save()
        Preorders.objects.create(user_info=order, order=bike)
        messages.add_message(request, messages.SUCCESS, "Your order is sent!")
        return HttpResponseRedirect(reverse('bikes:user'))
    return render(request, 'bikes/confirm_order.html', {'bike': bike})



@login_required
def users_orders(request):
    """show all orders from current user"""
    user = request.user
    order = models.Order.objects.get(name=user.username, email=user.email)
    preorders = models.Preorders.objects.filter(user_info=order)
    return render(request, 'bikes/user_orders.html', {'user':user, 'order': order, 'preorders': preorders})


@login_required
def order_details(request, pk):
    user = request.user
    order = get_object_or_404(models.Preorders, pk=pk)
    if order.user_info.email != user.email:
        return users_orders(request)
    return render(request,
                  'bikes/order_details.html',
                  {'user': user, 'order': order})


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
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successfully!")
    return HttpResponseRedirect(reverse('bikes:type'))