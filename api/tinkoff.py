import requests
from hashlib import sha256
from django.conf import settings


def init_payment(order_id: str) -> dict:
    submit_data = {
        "TerminalKey": settings.TINKOFF_TERMINAL_KEY,
        "Amount": settings.SUBSCRIPTION_PRICE,
        "OrderId": order_id,
        "Description": "Покупка подписки на сервис {сервис} на 30 дней",
        "SuccessURL": settings.TINKOFF_PAYMENT_SUCCESS_URL,
        "NotificationURL": settings.TINKOFF_PAYMENT_CALLBACK_URL,
        "PaymentObject": "payment"
    }
    submit_data['Token'] = generate_token(submit_data)
    return requests.post('https://securepay.tinkoff.ru/v2/Init', json=submit_data).json()


def generate_token(request_obj: dict) -> str:
    """
    :param request_obj: dict
    :return: hash: string

    https://www.tinkoff.ru/kassa/develop/api/request-sign/
    """
    obj = request_obj.copy()
    obj['Password'] = settings.TINKOFF_TERMINAL_PASSWORD
    exclude = ["Token", "Shops", "Receipt", "DATA"]
    keys = sorted(filter(lambda el: el not in exclude, obj.keys()))
    s = "".join([str(obj[key]) for key in keys])
    return sha256(s.encode("UTF-8")).hexdigest()

