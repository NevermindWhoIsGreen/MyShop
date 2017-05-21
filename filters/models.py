from django.db import models
from django.utils.translation import to_locale, get_language, ugettext_lazy as _
import uuid

from MyShop.models import (
    BaseModel,
    OrderingBaseModel,
    )
from django.utils.encoding import python_2_unicode_compatible, force_text




class FilterCategory(OrderingBaseModel):
    category = models.ForeignKey('Shop.Category', on_delete=models.CASCADE,
                                 related_name='filtercategories', verbose_name =_('Category'))
    slug = models.CharField(_("Slug"), default="", unique=True, max_length=250)
    name = models.CharField(_("Name"), default="", max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Filter Category')
        verbose_name_plural = _('Filters Category')


class FilterCar(OrderingBaseModel):
    category = models.ForeignKey('Shop.Car', on_delete=models.CASCADE,
                                 related_name='filtercar', verbose_name =_('Car'))
    slug = models.CharField(_("Slug"), default="", unique=True, max_length=250)
    name = models.CharField(_("Name"), default="", max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Filter Car')
        verbose_name_plural = _('Filters Car')


class FilterSelect(OrderingBaseModel):
    filter_category = models.ForeignKey(FilterCategory, on_delete=models.CASCADE,
                                        related_name='filterselect', verbose_name =_('Filter Category'))
    slug = models.CharField(_("Slug"), default="", unique=True,  max_length=250)
    name = models.CharField(_("Name"), default="", max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Filter Select')
        verbose_name_plural = _('Filters Select')


class ProductFilter(OrderingBaseModel):
    product = models.ForeignKey('Shop.Product', on_delete=models.CASCADE,
                                related_name='filterproducts', null=True, verbose_name =_('Product'))
    filter_category = models.ForeignKey(FilterCategory, on_delete=models.CASCADE, null=True,
                                        related_name='filter_select_product', verbose_name =_('Filter Category'))
    values = models.ManyToManyField(FilterSelect, related_name='filtervalues', blank=True, verbose_name =_('Values'))
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Product Filter')
        verbose_name_plural = _('Product Filters')
