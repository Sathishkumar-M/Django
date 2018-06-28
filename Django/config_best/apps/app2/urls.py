from django.conf.urls import url
from . import views

app_name = ''

urlpatterns = [
    url(r'^$',views.StudentListView.as_view(),name='student'),
]
