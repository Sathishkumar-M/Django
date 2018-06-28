from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, ListView, DetailView
from . import models

# Create your views here.

class SchoolListView(ListView):
    context_object_name = 'schools'
    model = models.School
