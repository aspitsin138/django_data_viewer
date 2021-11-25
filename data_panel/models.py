from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=300, unique=True, null=True, blank=True, verbose_name="Поставщик")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True, null=True, blank=True, verbose_name="Категория")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Brand(models.Model):
    name = models.CharField(max_length=300, unique=True, null=True, blank=True, verbose_name="Бренд")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class ItemUrl(models.Model):
    url = models.CharField(max_length=300, null=True, blank=True, verbose_name="Ссылка на страницу товара")

    def __str__(self):
        return f"{self.url}"

    class Meta:
        verbose_name = "Ссылка на товар"
        verbose_name_plural = "Ссылки на товар"


class Item(models.Model):
    provider = models.ForeignKey(Provider, null=True, blank=True, verbose_name="Поставщик", on_delete=models.SET_NULL)
    name = models.CharField(max_length=300, null=True, blank=True, verbose_name="Название товара")
    image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name="Ссылка на изображение")
    url = models.ForeignKey(ItemUrl, verbose_name="Ссылка на страницу товара", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, null=True, blank=True, verbose_name="Бренд", on_delete=models.SET_NULL)
    vendor_code = models.IntegerField(null=True, blank=True, verbose_name="Артикул")
    rating = models.IntegerField(null=True, blank=True, verbose_name="Рейтинг")
    reviews = models.IntegerField(null=True, blank=True, verbose_name="Количество отзывов")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена без скидки")
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                              verbose_name="Цена со скидкой")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Доступно")
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Категории")
    quantity_of_purchased = models.IntegerField(null=True, blank=True, verbose_name="Количество покупок")
    revenue = models.IntegerField(null=True, blank=True, verbose_name="Выручка")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} {self.brand} [{self.vendor_code}]"
