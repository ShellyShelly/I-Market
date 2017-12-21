from django.conf.urls import url
from shop import views


urlpatterns = [
    url(r'^$', views.IndexPageView.as_view(), name='ProductList'),
    url(r'^(?P<category_id>\d+)/$', views.IndexPageView.as_view(), name='ProductListByCategory'),
    url(r'^book/(?P<pk>\d+)/$', views.book_detail_view, name='BookDetail'),
    url(r'^author/(?P<pk>\d+)/$', views.AuthorDetailView.as_view(), name='AuthorDetail'),
]
