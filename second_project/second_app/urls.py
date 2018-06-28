from django.conf.urls import url
from second_app import views

urlpatterns = [
    url(r'^$',views.user,name='user'),
    url(r'^form/',views.formName,name='formName')
]
