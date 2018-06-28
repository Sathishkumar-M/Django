from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.
class LeaveRules(models.Model):
    leave_type = models.CharField(max_length=256,blank=False)
    leave_rules = models.TextField(blank=True,default='')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.leave_type
    # @property
    # def owner(self):
    #     return self.user

class LeaveApply(models.Model):
    user = models.ForeignKey(User,related_name='leaves')
    leave_type = models.ForeignKey(LeaveRules,related_name='leaves',null=True,blank=True)
    start_date = models.DateField(default=datetime.date.today, blank=True)
    end_date = models.DateField(default='', blank=True)
    no_of_days = models.DecimalField(max_digits=2,decimal_places=0,null=True)
    notes = models.TextField(blank=True,default='')
    tag_to = models.CharField(max_length=256,blank=False)
    status = models.CharField(max_length=256,default='Awaiting')
    status_by = models.CharField(max_length=256,default='')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.user.username
