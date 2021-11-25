from django.contrib import admin

from .models import Item, Category, Provider, Brand, ItemUrl

admin.site.register([Item, Category, Provider, Brand, ItemUrl])
