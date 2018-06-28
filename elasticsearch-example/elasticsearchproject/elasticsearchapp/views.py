from django.shortcuts import render,redirect,render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from . import models
from rest_framework import serializers
from django.http import JsonResponse
# from . import search
from elasticsearch_dsl import Search

# Create your views here.
class ElasticSearchListView(ListView):
    model = models.BlogPost
    template_name = 'elasticsearchapp/elasticsearch_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def post(self, request, *args, **kwargs):
        s = Search().filter('term', author=request.POST['author'])
        # context = s.execute()
        context = {"blogpost_list":s.execute()}
        return render(request,self.template_name,context)
