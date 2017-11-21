from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.searched_info, name='SearchedInfo'),
]