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
from . import forms
from rest_framework import serializers
from django.http import JsonResponse

# Create your views here.
class HolidayListView(LoginRequiredMixin,ListView):
    model = models.Holiday

    now = datetime.now()
    year = now.strftime("%Y")

    queryset = model.objects.filter(year__exact=year).order_by('holiday_date')

    year_list = model.objects.order_by('-year').values('year').distinct()

    template_name = 'holiday/holiday_list.html'

    def get(self, request, *args, **kwargs):
        context = locals()
        context['holiday_list'] = self.queryset
        context['year_list'] = self.year_list
        context['year'] = int(self.year)
        return render(request,self.template_name,context)
        # return render_to_response(self.template_name, context)


class HolidayUpdateView(LoginRequiredMixin,UpdateView):
    # fields = ('holiday_date','holiday_name','holiday_type','holiday_icon','note')
    model = models.Holiday
    form_class = forms.HolidayForm

    def get_object(self):
        model = models.Holiday
        return get_object_or_404(model,pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        registered = False
        model = models.Holiday
        # some_value = request.POST.get('pk')
        if request.method == 'POST':
            holiday_form = forms.HolidayForm(data=request.POST)
            if holiday_form.is_valid():
                obj = model.objects.get(pk=self.kwargs.get('pk'))
                if 'holiday_icon' in request.FILES:
                    obj.holiday_icon = request.FILES['holiday_icon']
                obj.holiday_date = datetime.strptime(request.POST['holiday_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
                obj.year = datetime.strptime(request.POST['holiday_date'], '%d/%m/%Y').strftime('%Y')
                obj.holiday_name = request.POST['holiday_name']
                obj.holiday_type = request.POST['holiday_type']
                obj.note = request.POST['note']

                obj.save()
                registered = True
                return redirect('holiday:list')
            else:
                print(holiday_form.errors)
        else:
            holiday_form = forms.HolidayForm

        return render(request,'holiday/holiday_form.html',
                                    {'form':holiday_form,
                                    'registered':registered})


class HolidayCreateView(LoginRequiredMixin,CreateView):
    form_class = forms.HolidayForm
    template_name = 'holiday/holiday_form.html'
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        registered = False
        if request.method == 'POST':
            holiday_form = forms.HolidayForm(data=request.POST)
            # print(holiday_form)
            if holiday_form.is_valid():
                holiday = holiday_form.save(commit=False)
                if 'holiday_icon' in request.FILES:
                    holiday.holiday_icon = request.FILES['holiday_icon']
                holiday.holiday_date = datetime.strptime(request.POST['holiday_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
                holiday.year = datetime.strptime(request.POST['holiday_date'], '%d/%m/%Y').strftime('%Y')

                holiday.save()

                registered = True
                return redirect('holiday:list')
            else:
                print(holiday_form.errors)
        else:
            holiday_form = forms.HolidayForm

        return render(request,'holiday/holiday_form.html',
                                    {'form':holiday_form,
                                    'registered':registered})

class HolidayDeleteView(DeleteView):
    model = models.Holiday
    success_url = reverse_lazy("holiday:list")

@login_required
def list_by_year(request):
    model = models.Holiday
    if request.method == 'POST':
        year = request.POST.get('year', None)
    else:
        now = datetime.now()
        year = now.strftime("%Y")

    queryset = model.objects.filter(year__exact=year).order_by('holiday_date')

    year_list = model.objects.order_by('-year').values('year').distinct()
    return render(request,'holiday/holiday_list.html',{'holiday_list':queryset,
                                                        'year_list':year_list,'year':int(year)})

class HolidaySerializer(serializers.Serializer):
    holiday_date = serializers.DateField()
    holiday_name = serializers.CharField(max_length=256)
    holiday_type = serializers.CharField(max_length=20)
    note = serializers.CharField(max_length=256)

def ajax_list(request):
    now = datetime.now()
    year = now.strftime("%Y")
    queryset = models.Holiday.objects.filter(year__exact=year)
    serializer = HolidaySerializer(queryset, many=True)
    data = {
        'list': serializer.data
    }
    return JsonResponse(data)
