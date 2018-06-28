from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from . import models

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class SchoolListView(ListView):
    context_object_name = 'schools'
    model = models.School

class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'basic_app/school_details.html'

class SchoolCreateView(CreateView):
    fields = ('name','principal','location')
    model = models.School

class SchoolUpdateView(UpdateView):
    model = models.School
    fields = ('name','principal')
    template_name = 'basic_app/school_form.html'

class SchoolDeleteView(DeleteView):
    model = models.School
    success_url = reverse_lazy("basic_app:list")
