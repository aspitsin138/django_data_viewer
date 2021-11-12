import django_filters

from .models import Item


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = {
            'price': ['lt', 'gt'],
            'price_with_discount': ['lt', 'gt'],
            'rating': ['lt', 'gt'],
            'reviews': ['lt', 'gt'],
            'revenue': ['lt', 'gt'],
        }
