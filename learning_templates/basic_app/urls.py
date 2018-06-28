from django.conf.urls import url
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    url(r'others/',views.others,name='others'),
    url(r'relative/',views.relative,name='relative')
]
