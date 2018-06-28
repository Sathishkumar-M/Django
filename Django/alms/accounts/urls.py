from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [

    url(r'login/$',auth_views.LoginView.as_view(template_name='accounts/login_form.html'),name='login'),
    url(r'logout/$',auth_views.LogoutView.as_view(),name='logout'),
    url(r'password/change/$', views.change_password,name='change_password'),
    url(r'ajax/validate_email/$', views.validate_email,name='validate_email'),
    # url(r'password/reset/$', auth_views.password_reset,{'template_name': 'accounts/password_reset_form.html'}, name='reset_password'),
    # url(r'password/reset/done/$',auth_views.password_reset_done,{'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
    # url(r'password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm,{'template_name': 'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
    # url(r'password/reset/complete/$',auth_views.password_reset_complete,{'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
]
