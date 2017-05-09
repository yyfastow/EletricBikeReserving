from django.contrib import admin

# Register your models here.
from shopping_cart import models


admin.site.register(models.Cart)
