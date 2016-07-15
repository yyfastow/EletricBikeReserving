from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from Bikes import models, forms
from EletricBikeReserving import settings


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


def order_bike(request, types_pk, bike_pk):
    """ makes form to order bike """
    bike = get_object_or_404(models.Bikes, pk=bike_pk)
    form = forms.OrderForm()
    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order = bike
            order.save()
            send_mail(
                "Order for {}".format(bike.name),
                """Bike: {}
                Name: {name}
                Phone Number: {phone}
                Billing Address: {address} {city} {state} {zip}
                    expiration: {expiration}
                    CCV number: {ccv_number}

                """.format(bike.name, **form.cleaned_data),
                '{name} <{email}>'.format(**form.cleaned_data),
                ['yoseffastow@gmail.com'],
            )
            # TODO: fix messages or better make a view confirming transaction and gives information about contacting
            messages.add_message(request, messages.SUCCESS, "Your order is sent!")
            return HttpResponseRedirect(reverse('bikes:type'))
    return render(request, 'bikes/order_form.html', {'form': form, 'bike': bike})
