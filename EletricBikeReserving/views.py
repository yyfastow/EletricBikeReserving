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
    return render(request, 'home.html', {"messages": messages})


@login_required
def delete_message(request, pk):
    user = request.user
    order = models.Order.objects.get(name=user.username, email=user.email)
    message = get_object_or_404(models.Message, pk=pk)
    message.delete(keep_parents=True)
    return HttpResponseRedirect(reverse('home'))