from django.urls import path

from api.views import add_goods, billing_callback, buy_subscription, categories_chart_data, provider_chart_data

urlpatterns = [
    path('goods/add', add_goods),
    path('billing/callback', billing_callback),
    path('subscription/buy', buy_subscription, name="buy-subscription"),
    path('chart/providers', provider_chart_data),
    path('chart/categories', categories_chart_data),
]