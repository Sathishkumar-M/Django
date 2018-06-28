from django.conf.urls import url
from . import views

app_name = 'holiday'

urlpatterns = [
    url(r'ajax/list/$', views.ajax_list,name='ajax_list'),
    url(r'list/$',views.HolidayListView.as_view(),name='list'),
    url(r'create/$',views.HolidayCreateView.as_view(),name='create'),
    url(r'update/(?P<pk>\d+)/$',views.HolidayUpdateView.as_view(),name='update'),
    url(r'delete/(?P<pk>\d+)/$',views.HolidayDeleteView.as_view(),name='delete'),
    url(r'list_by_year/$',views.list_by_year,name='list_by_year'),

]
