from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Course(models.Model):
    coursename = models.CharField(max_length=256,blank=False)
    describtion = models.TextField(blank=True,default='')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.coursename

class Fee(models.Model):
    course = models.ForeignKey(Course,related_name='course_fee')
    amount = models.DecimalField(max_digits=10,decimal_places=0,null=False)
    details = models.TextField(blank=True,default='')
    created_date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.course.coursename

class Student(models.Model):

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    course = models.ForeignKey(Course,related_name='student_course',blank=True, null=False,on_delete=models.PROTECT)
    firstname = models.CharField(max_length=256,blank=False)
    middlename = models.CharField(max_length=256,blank=True)
    lastname = models.CharField(max_length=256,blank=False)
    dob = models.DateField(blank=False)
    gender = models.CharField(max_length=10,choices=GENDER,default='Male')
    qualification = models.CharField(max_length=256,blank=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    phone = models.DecimalField(max_digits=15,decimal_places=0,null=True)
    city = models.CharField(max_length=256,blank=False)
    state = models.CharField(max_length=256,blank=False)
    country = models.CharField(max_length=256,blank=False)
    enroll_date = models.DateField(default=timezone.now)
    date_left_univ = models.DateField(blank=True,null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.firstname
