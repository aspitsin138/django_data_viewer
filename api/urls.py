from django.urls import path

from api.views import add_goods, billing_callback, buy_subscription

urlpatterns = [
    path('goods/add', add_goods),
    path('billing/callback', billing_callback),
    path('subscription/buy', buy_subscription, name="buy-subscription"),
]