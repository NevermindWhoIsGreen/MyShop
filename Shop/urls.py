from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ProductList, name='ProductList'),
    url(r'^search/$', views.search, name='search'),
    url(r'^ajax_search/$', views.ajax_search, name='ajax_search'),
    url(r'^car/(?P<car>[-\w]+)/$', views.car, name='ModelList'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='CategoryList'),
    url(r'^(?P<categoryMain_slug>[-\w]+)/(?P<category_slug>[-\w]+)/$', views.ProductListByCategory, name='ProductListByCategory'),
    url(r'^(?P<parent_slug>[-\w]+)/(?P<category_slug>[-\w]+)/(?P<id>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),

]
