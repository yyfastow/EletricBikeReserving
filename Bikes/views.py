from django.shortcuts import render, get_object_or_404

# Create your views here.
from Bikes import models


def bike_type_list(request):
    bike_types = models.BikeTypes.objects.all()
    return render(request,
                  'bikes/bike_types.html',
                    {'bike_types': bike_types})


def bike_list(request, pk):
    types = models.BikeTypes.objects.get(pk=pk)
    bikes = models.Bikes.objects.filter(type=types)
    return render(request,
                  'bikes/bike_list.html',
                  {'types': types, 'bikes': bikes})


def bike_details(request, types_pk, bike_pk):
    bike =get_object_or_404(models.Bikes,
                            type_id=types_pk,
                            pk=bike_pk)
    return render(request,
                  'bikes/bikes_details.html',
                  {'bike': bike})