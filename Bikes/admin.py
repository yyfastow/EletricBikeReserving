from django.contrib import admin

# Register your models here.
from Bikes import models

admin.site.register(models.BikeTypes)
admin.site.register(models.Bikes)
admin.site.register(models.Order)
admin.site.register(models.Preorders)
