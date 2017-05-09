from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from Bikes.forms import AmountForm, OrderForm, PasswordForm
from Bikes.models import Order, Bikes
from shopping_cart import models


def email_name_unique(request, name, email, user=None):
    """makes sure email and password is unique"""
    users_email = User.objects.filter(email=email)
    users_name = User.objects.filter(username=name)
    if users_email and user not in users_email:
        messages.error(request, "This email is all ready used by another user")
        return False
    elif users_name and user not in users_name:
        messages.error(
            request,
            "This name is all ready used by another costomer"
        )
        return False
    else:
        return True


@login_required
def add_to_cart(request, pk, amount=None):
    """ Adds bike to cart """
    bike = get_object_or_404(Bikes, pk=pk)
    amount_form = AmountForm(request.POST, empty_permitted=True)
    user = Order.objects.get(name=request.user.username)
    print(amount)
    if amount_form.is_valid() and amount is None:
        amount = amount_form.cleaned_data.get('amount')
        try:
            int(amount)
            print("amount is specified it its {}".format(amount))
        except:
            print("amount not specified")
            amount = 1
    total_price = amount * bike.price
    if models.Cart.objects.filter(user=user).filter(bike=bike):
        cart = models.Cart.objects.filter(user=user).get(bike=bike)

        cart.quantity += amount
        cart.price += total_price
        cart.save()
        messages.success(request, "Added more bikes to cart")
    else:
        models.Cart.objects.create(user=user, bike=bike, quantity=amount, price=total_price)
        messages.success(request, "Added to cart")
    return HttpResponseRedirect(reverse('cart:cart'))



@login_required
def show_cart(request):
    """shows item in cart """
    user = Order.objects.get(name=request.user.username)
    cart = models.Cart.objects.filter(user=user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required()
def remove_item_in_cart(request):
    """ removes one object from the cart that the user X'ed """
    pk = request.POST.get("pk")
    if not pk:
        return HttpResponseRedirect(reverse('cart:cart'))
    item = models.Cart.objects.get(pk=pk)
    if request.user.username != item.user.name:
        messages.error(request, "You cant delete that object its not in you cart")
        return redirect('/')
    item.delete(keep_parents=True)
    return HttpResponseRedirect(reverse('cart:cart'))


def register(request, pk):
    """ user registers and  than adds item to cart (For first time buyers that don't have an account)"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bikes:type'))
    form = OrderForm(request.POST or None)
    password = PasswordForm(request.POST or None)
    bike = Bikes.objects.get(pk=pk)
    amount_form = AmountForm(request.POST, empty_permitted=True)
    if form.is_valid() and password.is_valid() and amount_form.is_valid() and email_name_unique(
            request, form.cleaned_data['name'], form.cleaned_data['email']):
        amount = amount_form.cleaned_data.get('amount')
        """if not amount:
            print(amount_form)
            for item in amount_form:
                print(item)
            raise Http404"""
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
        return add_to_cart(request, pk, amount)
    return render(request, 'cart/registation_form.html',
              {'form': form, 'password': password, 'bike': bike, 'amount': amount_form})


@login_required()
def change_amount(request):
    """ Changes amount of bikes in cart. """
    pk = request.POST.get('pk')
    if not pk:
        return HttpResponseRedirect(reverse('cart:cart'))
    item = models.Cart.objects.get(pk=pk)
    if request.user.username != item.user.name:
        messages.error(request, "You cant change value of this item its not in your cart")
        return redirect('/')
    bike = Bikes.objects.get(pk=item.bike_id)
    old_price = round(float(item.price) * 100)/100
    amount = AmountForm(request.POST)
    if amount.is_valid():
        total = bike.price * amount.cleaned_data.get('amount')
        item.quantity = amount.cleaned_data['amount']
        item.price = total
        item.save()
        if request.is_ajax():
            price = round(float(total) * 100)/100
            return JsonResponse({
                'price': price,
                'old_price': old_price,
                'amount': item.quantity,
            })
        else:
            messages.success(request, "changed amount")
    return HttpResponseRedirect(reverse('cart:cart'))


# @login_required()
# def update_cart(request):
#     """ update  """
#     user = Order.objects.get(name=request.user.username)
#     cart = models.Cart.objects.filter(user=user)
#     for item in cart:
#         bike = Bikes.objects.get(pk=item.bike_id)
#         amount = AmountForm(bike.name)
#         if amount.is_valid():
#             total = bike.price * amount.cleaned_data['amount']
#             item.quantity = amount.cleaned_data['amount']
#             item.price = total
#             item.save()
#     return HttpResponseRedirect(reverse('cart:cart'))
