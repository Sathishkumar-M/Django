"""alms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
# from django.contrib.auth.forms import AdminPasswordChangeForm

urlpatterns = [
    url(r'^$',views.HomePage.as_view(),name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',include('accounts.urls',namespace='accounts')),
    url(r'^test/$',views.TestPage.as_view(),name='test'),
    url(r'^thanks/$',views.ThanksPage.as_view(),name='thanks'),
    url(r'^employee/',include('employee.urls',namespace='employee')),
    url(r'^leave/',include('leave.urls',namespace='leave')),
    url(r'^holiday/',include('holiday.urls',namespace='holiday')),
    url(r'^accounts/password/reset/$', auth_views.password_reset,{'template_name': 'accounts/password_reset_form.html'}, name='reset_password'),
    url(r'^accounts/password/reset/done/$',auth_views.password_reset_done,{'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm,{'template_name': 'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$',auth_views.password_reset_complete,{'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
]
