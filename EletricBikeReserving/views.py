from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from Bikes import models, forms


def home(request):
    messages = []
    if request.user.is_authenticated():
        user = request.user
        if user.is_superuser:
            messages = models.Message.objects.filter(owner="to")
        else:
            order = models.Order.objects.get(name=user.username, email=user.email)
            messages = models.Message.objects.filter(user=order, owner="from")
        return render(request, 'home.html', {"your_messages": messages})
    else:
        return HttpResponseRedirect(reverse('bikes:type'))


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
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """logs out user"""
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successfully!")
    return HttpResponseRedirect(reverse('bikes:type'))


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
    return render(request, 'admin_messages.html', {'message': message})


@login_required
def delete_message(request):
    pk = request.POST.get('pk')
    user = request.user
    if not user.is_superuser:
        order = models.Order.objects.get(name=user.username, email=user.email)
    message = get_object_or_404(models.Message, pk=pk)
    message.delete(keep_parents=True)
    return HttpResponseRedirect(reverse('home'))
