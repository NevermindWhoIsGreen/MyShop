from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
import mptt
from django.core.urlresolvers import reverse


# Модель категории
class Category(MPTTModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name='Родительский класс')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('tree_id','level')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_py = ['name']

    def get_absolute_url(self):
        return reverse('shop:CategoryList', args=[self.slug])

mptt.register(Category,order_insertion_py=['name'])


# Модель продукта
class Product(models.Model):
    category = TreeForeignKey(Category, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Изображение товара")
#    description = models.TextField(blank=True, verbose_name="Описание")
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="На складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductDetail', args=[self.id, self.slug])