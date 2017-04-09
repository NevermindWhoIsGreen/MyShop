from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ProductList, name='ProductList'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='CategoryList'),
    url(r'^(?P<categoryMain_slug>[-\w]+)/(?P<category_slug>[-\w]+)/$', views.ProductListByCategory, name='ProductListByCategory'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
]
