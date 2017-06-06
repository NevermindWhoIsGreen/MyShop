from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from properties.models import ProductProperty, CategoryProperty
from filters.models import ProductFilter, FilterCategory
from django.core.urlresolvers import reverse

from MyShop.models import (
    BaseModel,
    OrderingBaseModel,
)


# Модель категории
class Category(MPTTModel, OrderingBaseModel):
    slug = models.CharField(_("Slug"), default="", unique=True, max_length=250)
    name = models.CharField(_("Name"), default="", max_length=250)
    title = models.CharField(_("Title"), blank=True, default="", max_length=250)
    description = models.CharField(_("Description"), blank=True, default="", max_length=250)
    keywords = models.CharField(_("Keywords"), blank=True, default="", max_length=250)
    parent = TreeForeignKey('self', null=True, blank=True,  related_name='children', verbose_name=_('Parent'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:CategoryList', args=[self.slug])

    def get_absolute_url_with_parent(self):
        return reverse('shop:ProductListByCategory', args=[self.parent.slug, self.slug])


# Модель машины
class Car(MPTTModel, OrderingBaseModel):
    slug = models.CharField(_("Slug"), default="", unique=True, max_length=250)
    name = models.CharField(_("Name"), default="", max_length=250)
    title = models.CharField(_("Title"), blank=True, default="", max_length=250)
    description = models.TextField(_("Description"), blank=True, default="", max_length=250)
    keywords = models.CharField(_("Keywords"), blank=True, default="", max_length=250)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('Parent'))

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ModelList', args=[self.slug])


# Модель продукта
class Product(OrderingBaseModel):
    category = TreeForeignKey(Category, on_delete=models.CASCADE, related_name='categories', blank=True, null=True,
                              verbose_name=_('Category'))
    car = TreeForeignKey(Car, on_delete=models.CASCADE, related_name='cars', blank=True, null=True,
                         verbose_name=_('Car'))
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="На складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    url = models.CharField(_("Url"), default="", blank=True, max_length=250)
    keywords = models.CharField(_("Keywords"), blank=True, default="", max_length=250)

    def save(self, *args, **kwargs):
        if self.category:
            super(Product, self).save(*args, **kwargs)
            # we create properties if not exist
            for cp in CategoryProperty.objects.filter(category=self.category):
                pp = ProductProperty.objects.filter(category_property=cp,
                                                    product=self)
                if not pp:
                    pp = ProductProperty(category_property=cp, product=self, value="--")
                    pp.save()
            # we create filters if not exist
            for fc in FilterCategory.objects.filter(category=self.category):
                pf = ProductFilter.objects.filter(filter_category=fc,
                                                  product=self)
                if not pf:
                    pf = ProductFilter(filter_category=fc, product=self)
                    pf.save()


    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('shop:ProductDetail', args=[self.id, self.slug])
        return reverse('shop:ProductDetail', args=[self.category.parent.slug, self.category.slug, self.id])

# Модель предложений
class Offer(OrderingBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', null=True,
                                verbose_name=_('Product'))
    name = models.CharField(_("Name"), default="", max_length=250)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00, verbose_name=_('Price'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Offer')
        verbose_name_plural = _('Offers')