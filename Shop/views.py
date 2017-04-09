from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Страница с товарами
def ProductList(request, category_slug=None):
    category = None
    catChilds = None
    categories = Category.objects.get(id=34)
    categories = categories.get_children()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        catChilds = category.get_children()
        # products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'catChilds':catChilds,
    })

# Страница товара
def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})

def ProductListByCategory(request, categoryMain_slug, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/ListByCategory.html', {
        'category' : category,
        'products' : products
    })
