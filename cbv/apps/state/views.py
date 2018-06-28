from django.shortcuts import render
from django.views.generic import View, ListView
from . import models

# Create your views here.

class SchoolListView(ListView):
    context_object_name = 'schools'
    model = models.School
