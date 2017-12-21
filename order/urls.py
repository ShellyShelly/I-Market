from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'make_order/$', views.MakeOrder.as_view(), name='MakeOrder'),
    url(r'^confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_order, name='ConfirmOrder'),
]