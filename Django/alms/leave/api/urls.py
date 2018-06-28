from django.conf.urls import url
from .views import LeaveRulesRudView, LeaveRulesAPIView

urlpatterns = [
    url(r'^$',LeaveRulesAPIView.as_view(),name='post-create'),
    url(r'^(?P<pk>\d+)/$',LeaveRulesRudView.as_view(),name='post-rud')
]
