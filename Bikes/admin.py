from django.contrib import admin

# Register your models here.
from Bikes import models


class BikeAdmin(admin.ModelAdmin):
    search_fields = ['type', 'price', 'name']
    list_filter = ['type', 'price']


    class Meta:
        model = models.Bikes


class BillingAdmin(admin.ModelAdmin):
    # list_display = []
    search_fields = ['state', 'city', 'address', 'user_info', 'zip']
    list_filter = ['user_info']

    class Meta:
        model = models.Billing


class CardAdmin(admin.ModelAdmin):
    list_display = ['number', 'expiration', 'ccv_number', 'user_info']
    search_fields = ['number', 'expiration', 'ccv_number', 'user_info']
    list_filter = ['user_info']

    class Meta:
        model = models.Card


class PreorderAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'order', 'status']
    search_fields = ['user_info', 'order', 'status']
    list_filter = ['user_info', 'order', 'status']

    class Meta:
        model = models.Preorders


admin.site.register(models.BikeTypes)
admin.site.register(models.Bikes, BikeAdmin)
admin.site.register(models.Order)
admin.site.register(models.Billing, BillingAdmin)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.Preorders, PreorderAdmin)
admin.site.register(models.Message)

