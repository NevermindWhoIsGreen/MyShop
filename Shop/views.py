from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product
from cart.forms import CartAddProductForm


# Страница каталога
def ProductList(request, category_slug=None):
    category = None
    catChilds = None
    categories = Category.objects.get(id=34)
    categories = categories.get_children()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        catChilds = category.get_children()
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'catChilds':catChilds,
    })


#Страница товаров по категории
def ProductListByCategory(request, categoryMain_slug, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(available=True, category=category)
    return render(request, 'shop/product/ListByCategory.html', {
        'category' : category,
        'products' : products
    })


# Страница товара
def ProductDetail(request, parent_slug, category_slug, id):
    product = get_object_or_404(Product, id=id, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form
                                                        })



