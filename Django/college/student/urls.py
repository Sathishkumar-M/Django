from django.conf.urls import url, include
from . import views

app_name = 'school'

urlpatterns = [
        url(r'api/student/',include('student.api.urls', namespace='api-postings')),
]
