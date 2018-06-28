from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    url(r'^$',views.PostList.as_view(),name='all'),
    url(r'new/$',views.CreatePost.as_view(),name='create'),
    url(r'^edit/(?P<pk>\d+)/$',views.PostUpdateView.as_view(),name='post_edit'),
    # url(r'by/(?P<username>[-\w]+)',views.UserPosts.as_view(),name='for_user'),
    # url(r'by/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.PostDetail.as_view(),name='single'),
    url(r'delete/(?P<pk>\d+)/$',views.DeletePost.as_view(),name='delete'),
]
