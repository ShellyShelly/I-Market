from django.conf.urls import url, include
from django.contrib import admin
from shop import urls as shop_urls
from cart import urls as cart_urls
from search import urls as search_urls
from account import urls as account_urls
from IMarket import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^shop/', include(shop_urls, namespace='shop')),
    url(r'^cart/', include(cart_urls, namespace='cart')),
    url(r'^search/', include(search_urls, namespace='search')),
    url(r'^account/', include(account_urls, namespace='account')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
