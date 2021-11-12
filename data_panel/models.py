from django.db import models


class Item(models.Model):
    provider = models.CharField(max_length=300, null=True, blank=True, verbose_name="Поставщик")
    name = models.CharField(max_length=300, null=True, blank=True, verbose_name="Название товара")
    image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name="Ссылка на изображение")
    url = models.CharField(max_length=300, null=True, blank=True, verbose_name="Ссылка на страницу товара")
    brand = models.CharField(max_length=300, null=True, blank=True, verbose_name="Бренд")
    vendor_code = models.IntegerField(null=True, blank=True, verbose_name="Артикул")
    rating = models.IntegerField(null=True, blank=True, verbose_name="Рейтинг")
    reviews = models.IntegerField(null=True, blank=True, verbose_name="Количество отзывов")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена без скидки")
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                              verbose_name="Цена со скидкой")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Доступно")
    categories = models.CharField(null=True, blank=True, max_length=500, verbose_name="Рубрики")
    quantity_of_purchased = models.IntegerField(null=True, blank=True, verbose_name="Количество покупок")
    revenue = models.IntegerField(null=True, blank=True, verbose_name="Выручка")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} {self.brand} [{self.vendor_code}]"
