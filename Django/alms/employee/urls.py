from django.conf.urls import url
from . import views

app_name = 'employee'

urlpatterns = [
    url(r'ajax/list/$', views.ajax_list,name='ajax_list'),
    url(r'list/$',views.List.as_view(),name='list'),
    url(r'^registration/$',views.Registration.as_view(),name='registration'),
    url(r'^update/(?P<pk>\d+)/$',views.EmployeeUpdateView.as_view(),name='update'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'delete/(?P<pk>\d+)/$',views.delete_employee,name='delete'),

]
