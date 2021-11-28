from django.contrib import admin

from .models import Item, Category, Provider, Brand, ItemUrl, Subscription, PaymentsInfo

admin.site.register([Item, Category, Provider, Brand, ItemUrl, Subscription, PaymentsInfo])
