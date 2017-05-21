from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product, Car
from cart.forms import CartAddProductForm
from properties.models import ProductProperty, CategoryProperty
from filters.models import ProductFilter, FilterCategory, FilterSelect
from django.db.models import Q

# Страница каталога
def ProductList(request, category_slug=None):
    category = None
    catChilds = None
    categories = Category.objects.get(id=1)
    categories = categories.get_children()
    cars = Car.objects.get(id=2)
    cars = cars.get_children()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        catChilds = category.get_children()
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'catChilds':catChilds,
        'cars':cars,
    })


# Страница товаров по категории
def ProductListByCategory(request, categoryMain_slug, category_slug):
    FF = request.GET
    target=[]
    for key, value in FF.items():
        k = value.split('|')
        for i in k:
            target.append(i)

    category = get_object_or_404(Category, slug=category_slug)
    category_filters = FilterCategory.objects.filter(category=category)

    product_filter = []
    for k in target:
        product_filter.append(FilterSelect.objects.get(slug=k))

    filtered_products = []
    for k in product_filter:
        test=ProductFilter.objects.filter(values=k)
        for i in test.values():
            filtered_products.append(i['product_id'])
    filtered_products=set(filtered_products)

    filters_select = {}
    for filter in category_filters:
        filter_select = FilterSelect.objects.filter(filter_category=filter)
        filters_select.update({filter : filter_select})
    products = Product.objects.filter(available=True, category=category)
    return render(request, 'shop/product/ListByCategory.html', {
        'category' : category,
        'products' : products,
        'category_filters' : category_filters,
        'filters_select' : filters_select,
        'product_filter' : product_filter,
        'filtered_products' : filtered_products,
    })


# Страница товара
def ProductDetail(request, parent_slug, category_slug, id):
    product = get_object_or_404(Product, id=id, available=True)
    category_property = CategoryProperty.objects.filter(category=product.category)
    product_property = ProductProperty.objects.filter(product=product)
    desc_list = zip(category_property,product_property)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'category_property': category_property,
                                                        'product_property':product_property,
                                                        'cart_product_form': cart_product_form,
                                                        'desc_list' : desc_list,
                                                        })

# Поиск товаров
def search_product(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
    else:
        search_query = ''

    products = Product.objects.filter(Q(name__icontains=search_query))

    content = {}
    content['products'] = products

    return render(request, 'shop/product/search_result.html', content)