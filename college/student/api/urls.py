from django.conf.urls import url,include
from .views import StudentAPIView, StudentRudView,CourseAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', StudentAPIView,base_name='user')
# router.register(r'users', views.UserViewSet)

# snippet_list = StudentAPIView.as_view({
#     'get': 'list',
#     'post': 'create'
# })

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^$', snippet_list, name='post-create'),
    # url(r'^$',StudentAPIView.as_view(),name='post-create'),
    url(r'^(?P<pk>\d+)/$',StudentRudView.as_view(),name='post-rud'),
    url(r'^course/$',CourseAPIView.as_view(),name='course-list'),
]
