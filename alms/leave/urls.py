from django.conf.urls import url, include
from . import views

app_name = 'leave'

urlpatterns = [
    url(r'rules/list/$',views.List.as_view(),name='list'),
    url(r'rules/detail/(?P<pk>\d+)/$',views.LeaveRulesDetail.as_view(),name='detail'),
    url(r'rules/create/$',views.LeaveRulesCreateView.as_view(),name='create'),
    url(r'rules/update/(?P<pk>\d+)/$',views.LeaveRulesUpdateView.as_view(),name='update'),
    url(r'rules/delete/(?P<pk>\d+)/$',views.LeaveRulesDeleteView.as_view(),name='delete'),
    url(r'apply/$',views.LeaveApplyCreateView.as_view(),name='apply'),
    url(r'applied/$',views.LeaveAppliedListView.as_view(),name='applied'),
    url(r'applied/(?P<username>[-\w]+)/$',views.LeaveAppliedUserListView.as_view(),name='applied_leave'),
    url(r'draft/(?P<username>[-\w]+)/$',views.LeaveDraftListView.as_view(),name='draft'),
    url(r'apply/update/(?P<pk>\d+)/$',views.LeaveApplyUpdateView.as_view(),name='apply_update'),
    url(r'apply/delete/(?P<pk>\d+)/$',views.LeaveApplyDeleteView.as_view(),name='apply_delete'),
    url(r'status/(?P<status>[0-9A-Za-z_\-]+)/(?P<approve_by>[0-9A-Za-z_\-]+)/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<lidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.status, name='status'),
        url(r'ajax/leave_status/$', views.leave_status,name='leave_status'),
        url(r'api/postings/',include('leave.api.urls', namespace='api-postings')),
]
