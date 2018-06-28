from django.conf.urls import url
from .views import formView,login

app_name = ''

urlpatterns = [
    url(r'^connection/', formView),
    url(r'^login/', login, name = 'login'),
]