import os
from collections import defaultdict

from django.conf import settings

from data_panel.models import ItemUrl, Item


def get_item_query():
    use_sqlite = os.environ.get("USE_SQLITE", "true").lower() == "true"

    if use_sqlite:
        item_ids = []
        for url in ItemUrl.objects.iterator(chunk_size=settings.QUERYSET_CHUNK_SIZE):
            item_ids.append(url.item_set.latest('created_at').id)
        return Item.objects.filter(id__in=item_ids)
    else:
        item_ids_query = Item.objects.order_by('url', '-created_at').distinct('url').only('id').all()
        return Item.objects.filter(id__in=item_ids_query)


def get_chart_data(rel_field: str, value_field: str, many_to_many=False) -> dict:
    computed = defaultdict(float)
    fresh_items = get_item_query()

    for item in fresh_items.iterator(chunk_size=settings.QUERYSET_CHUNK_SIZE):
        value = getattr(item, value_field)
        rel_model = getattr(item, rel_field)

        if (not value) or (not rel_model):
            continue

        if not many_to_many:
            computed[rel_model.name] += float(value)
            continue

        for rel in rel_model.iterator(chunk_size=settings.QUERYSET_CHUNK_SIZE):
            computed[rel.name] += float(value)

    raw_data = [*computed.items()]

    sorted_data = sorted(raw_data, key=lambda x: -x[1])
    labels = list(map(lambda x: x[0], sorted_data[:6]))
    data = list(map(lambda x: x[1], sorted_data[:6]))

    labels.append("Остальное")
    data.append(sum([i[1] for i in sorted_data[6:]]))

    colors = ["#fe6383", "#3a9fed", "#4ec0b6", "#fd9c3b", "#fec95f", "#a264f5"]

    response = {
        "labels": labels,
        "values": data,
        "colors": colors[:len(data) - 1] + ["#c8cbda"]
    }
    return response
