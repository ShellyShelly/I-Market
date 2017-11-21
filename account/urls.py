from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^profile/(?P<pk>\d+)/$', views.AccountDetailView.as_view(), name='AccountDetail'),
    url(r'^profile/update/(?P<pk>\d+)/$', views.AccountUpdateView.as_view(), name='AccountUpdate'),
    url(r'^login/$', views.LoginView.as_view(), name='Login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='Logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='SignUp'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='ActivateAccount'),
]
