import os

from django.db.models import OuterRef, Sum

from data_panel.models import ItemUrl, Item


def get_item_query():
    use_sqlite = os.environ.get("USE_SQLITE", "true").lower() == "true"

    if use_sqlite:
        item_ids = []
        for url in ItemUrl.objects.iterator():
            item_ids.append(url.item_set.latest('created_at').id)
        return Item.objects.filter(id__in=item_ids)
    else:
        item_ids_query = Item.objects.order_by('url', '-created_at').distinct('url').only('id').all()
        return Item.objects.filter(id__in=item_ids_query)


def get_chart_data(model, rel_field: str, field: str) -> dict:
    items = get_item_query()

    item_query = items.filter(**dict(((rel_field, OuterRef('pk')),))).values(f'{rel_field}__pk')
    field_sum_query = item_query.annotate(field_sum=Sum(field)).values("field_sum")
    model_instances = model.objects.annotate(field_sum=field_sum_query).order_by(f"-field_sum")

    labels = []
    values = []
    colors = ["#fe6383", "#3a9fed", "#4ec0b6", "#fd9c3b", "#fec95f", "#a264f5", "#c8cbda"]

    for instance in model_instances[:6]:
        labels.append(instance.name)
        values.append(float(instance.field_sum))

    if len(model_instances[6:]):
        labels.append("Остальное")
        values.append(float(model_instances[6:].aggregate(t=Sum('field_sum'))['t']))

    return {
        "labels": labels,
        "values": values,
        "colors": colors[:len(values)]
    }
