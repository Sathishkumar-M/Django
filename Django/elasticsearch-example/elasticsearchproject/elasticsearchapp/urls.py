from django.conf.urls import url
from . import views

app_name = ''

urlpatterns = [
    url(r'list/$',views.ElasticSearchListView.as_view(),name='list'),
]
