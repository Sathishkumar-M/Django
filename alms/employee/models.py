from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class EmployeeProfileInfo(models.Model):
    user = models.OneToOneField(User)
    #additional
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    age = models.PositiveIntegerField(blank=False)
    phone = models.PositiveIntegerField(blank=False)
    address = models.TextField(blank=True,default='')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
