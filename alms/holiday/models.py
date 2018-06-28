from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime

# Create your models here.
class Holiday(models.Model):
    holiday_date = models.DateField(default=datetime.date.today, blank=True)
    year = models.DecimalField(max_digits=4,decimal_places=0,null=True)
    holiday_name = models.CharField(max_length=256,blank=False)
    HOLIDAY_CHOICES =(
            ('Genral','Genral'),
            ('Restricted','Restricted')
    )

    holiday_type = models.CharField(max_length=20,choices=HOLIDAY_CHOICES,default='Genral')
    holiday_icon = models.ImageField(upload_to='holiday_icon',blank=True)
    note = models.CharField(max_length=256,blank=True,default='')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['holiday_date']

    def __str__(self):
        return self.holiday_name

    def get_absolute_url(self):
        return reverse('holiday:list')
