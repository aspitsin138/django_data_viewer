import json
from datetime import timedelta
from math import trunc

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from api.tinkoff import generate_token, init_payment
from data_panel.helpers import get_chart_data
from data_panel.models import PaymentsInfo, Brand, Provider, Category, Item, ItemUrl


@csrf_exempt
def billing_callback(request):
    data = json.loads(request.body)

    print(generate_token(data))

    if data.get('Token') != generate_token(data):
        return HttpResponse(status=403, content="Forbidden")

    user_id, timestamp = map(int, data['OrderId'].split('_'))

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=403, content="Forbidden")

    payment = PaymentsInfo.objects.create(
        user=user,
        amount=data.get("Amount", 0),
        status=data.get("Status", "")
    )

    payment.save()

    # if user have active trial version
    if user.subscription.is_trial and user.subscription.is_active():
        user.subscription.is_trial = False
        user.subscription.valid_until += timedelta(days=30)
        user.save()
    elif not user.subscription.is_active():
        user.subscription.is_trial = False
        user.subscription.valid_until = timezone.now() + timedelta(days=30)
        user.save()

    return HttpResponse(status=200, content="OK")


@login_required
def buy_subscription(request):
    if request.user.subscription.is_active() and not request.user.subscription.is_trial:
        return redirect('billing')

    info = init_payment(f"{request.user.id}_{trunc(timezone.now().timestamp())}")

    if info['Success']:
        return redirect(info['PaymentURL'])


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
def categories_chart_data(request):
    return JsonResponse({
        "chart1": get_chart_data("categories", "quantity_of_purchased", many_to_many=True),
        "chart2": get_chart_data("categories", "revenue", many_to_many=True)
    })


@login_required
def provider_chart_data(request):
    return JsonResponse({
        "chart1": get_chart_data("provider", "quantity_of_purchased"),
        "chart2": get_chart_data("provider", "revenue")
    })
