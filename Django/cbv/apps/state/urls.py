from django.conf.urls import url
from . import views

app_name = ''

urlpatterns = [
    url(r'^$',views.SchoolListView.as_view(),name='list'),
]
