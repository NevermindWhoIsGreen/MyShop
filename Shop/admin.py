from django.contrib import admin
from .models import Category, Product
from mptt.admin import MPTTModelAdmin

# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','id']
    prepopulated_fields = {'slug': ('name', )}
# Модель товара

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
