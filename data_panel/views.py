import json
import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import QueryDict, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.views import FilterView

from .filters import ItemFilter
from .forms import UserRegisterForm
from .models import Item, Brand, Category, Provider, ItemUrl
from .mixins import SubscriptionRequiredMixin


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign-in')
    else:
        form = UserRegisterForm()
    return render(request, 'sign-up.html', {'form': form})


@csrf_exempt
def add_goods(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            request_key = data.pop('API_KEY', None)
            if request_key != settings.API_KEY:
                return HttpResponse(status=403)

            for key, value in data.items():
                if value == "":
                    data[key] = None

            if data['url']:
                data['url'] = ItemUrl.objects.get_or_create(url=data['url'])[0]
            else:
                del data['url']

            if data['brand']:
                data['brand'] = Brand.objects.get_or_create(name=data['brand'])[0]
            else:
                del data['brand']

            if data['provider']:
                data['provider'] = Provider.objects.get_or_create(name=data['provider'])[0]
            else:
                del data['provider']

            categories = []

            if data['categories']:
                for cg in data['categories'].split("/"):
                    categories.append(Category.objects.get_or_create(name=cg.strip())[0])
            del data['categories']

            item = Item(**data)
            item.save()
            item.categories.set(categories)
            return HttpResponse(status=200, content="OK")
        except Exception as e:
            print(e)
            return HttpResponse(status=406)
    else:
        return HttpResponse(status=405)


@login_required
def billing(request):
    return render(request, 'billing.html')


class ItemListView(LoginRequiredMixin, SubscriptionRequiredMixin, FilterView):
    template_name = 'item_list.html'
    paginate_by = 25
    model = Item
    filterset_class = ItemFilter

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
