from django.conf.urls import url

from .views import BlogView

urlpatterns = [
    url(
        regex=r'^api/list$',
        view=BlogView.as_view(),
        name='blog-list'
    ),
]
