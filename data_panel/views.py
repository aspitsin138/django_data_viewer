import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import QueryDict
from django.shortcuts import render
from django_filters.views import FilterView

from .filters import ItemFilter
from .helpers import get_item_query
from .mixins import SubscriptionRequiredMixin
from .models import Item


@login_required
def billing(request):
    return render(request, 'billing.html')


class ItemListView(LoginRequiredMixin, SubscriptionRequiredMixin, FilterView):
    template_name = 'item_list.html'
    paginate_by = 25
    model = Item
    filterset_class = ItemFilter

    queryset = get_item_query()

    def get_context_data(self, **kwargs):
        table_headers = [
            {"id": "name", "name": "Товар"},
            {"id": "brand", "name": "Бренд"},
            {"id": "provider", "name": "Поставщик"},
            {"id": "rating", "name": "Рейтинг"},
            {"id": "reviews", "name": "Отзывы"},
            {"id": "price_with_discount", "name": "Цена"},
            {"id": "quantity", "name": "Доступно"},
            {"id": "categories", "name": "Категории"},
            {"id": "quantity_of_purchased", "name": "Куплено"},
            {"id": "revenue", "name": "Выручка"}
        ]

        ordering = self.request.GET.get('order_by', None)

        for header in table_headers:
            query = QueryDict(self.request.GET.urlencode(), mutable=True)

            if ordering == f"-{header['id']}":
                query["order_by"] = f"{header['id']}"
            elif ordering != header['id']:
                query["order_by"] = f"-{header['id']}"
            else:
                query["order_by"] = ""

            query['page'] = 1
            header['url'] = f"?{query.urlencode()}"

        if ordering:
            match_obj = re.match(r'-?(.+)', ordering)
            order_field = match_obj.groups()[0]
            order_field_index = next((index for (index, d) in enumerate(table_headers) if d["id"] == order_field), None)
            table_headers[order_field_index]["active"] = True
            table_headers[order_field_index]["down"] = ordering != order_field

        context = super().get_context_data(**kwargs)
        context['object_list'] = context['object_list'].iterator(
            chunk_size=settings.QUERYSET_CHUNK_SIZE
        )
        context['table_headers'] = table_headers
        return context

    def get_ordering(self):
        fields = [
            "id", "provider", "name", "brand", "vendor_code",
            "rating", "reviews", "price", "price_with_discount",
            "quantity", "categories", "quantity_of_purchased", "revenue"
        ]
        ordering = self.request.GET.get('order_by', 'id')

        match_obj = re.match(r'-?(.+)', ordering)

        if match_obj and (match_obj.groups()[0] in fields):
            field = match_obj.groups()[0]

            if field == ordering:
                return [F(field).asc(nulls_first=True)]
            else:
                return [F(field).desc(nulls_last=True)]

        return 'id'
