from django.contrib import admin
from .models import Category, Product, Offer
from mptt.admin import MPTTModelAdmin
from properties.models import CategoryProperty, ProductProperty
from filters.models import FilterCategory, ProductFilter, FilterSelect
from django.forms import TextInput, ModelForm, Textarea, Select


class CategoryPropertyInline(admin.TabularInline):
    model = CategoryProperty
    extra = 1
    verbose_name_plural = 'Params'
    suit_classes = 'suit-tab suit-tab-params'


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 1
    verbose_name_plural = 'Params'
    suit_classes = 'suit-tab suit-tab-params'


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1
    verbose_name_plural = 'Offers'
    suit_classes = 'suit-tab suit-tab-offers'


class ProductFilterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        if self.instance:
            i = self.instance
            if i.filter_category:
                self.fields["values"].queryset = \
                    FilterSelect.objects.filter(filter_category=i.filter_category)

    class Meta:
        model = ProductFilter
        fields = '__all__'


class ProductFilterInline(admin.TabularInline):
    form = ProductFilterForm
    model = ProductFilter
    extra = 1
    verbose_name_plural = 'Filters'
    suit_classes = 'suit-tab suit-tab-filters'


class FilterCategoryInline(admin.TabularInline):
    model = FilterCategory
    extra = 1
    verbose_name_plural = 'Filters'
    suit_classes = 'suit-tab suit-tab-filters'

    def get_prepopulated_fields(self, request, obj=None):
        # can't use `prepopulated_fields = ..` because it breaks the admin validation
        # for translated fields. This is the official django-parler workaround.
        return {
            'slug': ('name',)
        }


# Модель категории
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    inlines = [CategoryPropertyInline, FilterCategoryInline, ]
    suit_form_tabs = (('general', 'General'),
                      ('params', 'Params'),
                      ('filters', 'Filters'))
    fieldsets = [
        ('General', {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'name',
                'slug',
                'title',
                'description',
                'keywords',
                'parent',
            ]
        }),
    ]

    def get_prepopulated_fields(self, request, obj=None):
        # can't use `prepopulated_fields = ..` because it breaks the admin validation
        # for translated fields. This is the official django-parler workaround.
        return {
            'slug': ('name',)
        }


# Модель товара
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPropertyInline,
               OfferInline,
               ProductFilterInline
               ]
    list_display = ('name', 'category', 'published')
    suit_form_tabs = (('general', 'General'),
                      ('offers', 'Offers'),
                      ('params', 'Params'),
                      ('filters', 'Filters'),
                      ('images', 'Images'),)
    fieldsets = [
        ('General', {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['name',
                       'slug',
                       'description',
                       'keywords',
                       'image',
                       'category',
                       'price', ]
        }),
    ]

    def get_prepopulated_fields(self, request, obj=None):
        # can't use `prepopulated_fields = ..` because it breaks the admin validation
        # for translated fields. This is the official django-parler workaround.
        return {
            'slug': ('name',)
        }
