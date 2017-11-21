from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.cart_detail, name='CartDetail'),
    url(r'^remove/(?P<product_id>\d+)/$', views.remove_product_from_cart, name='RemoveProductFromCart'),
    url(r'^add/(?P<product_id>\d+)/$', views.add_product_to_cart, name='AddProductToCart'),
    url(r'clear/$', views.clear_cart, name='ClearCart'),
]
