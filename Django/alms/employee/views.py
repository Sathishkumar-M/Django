from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from employee.models import User,EmployeeProfileInfo
from django.http import HttpResponseRedirect, HttpResponse
from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from . import forms
from . import models
import random
import string
from django.http import JsonResponse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from employee.tokens import account_activation_token

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from rest_framework import serializers
# Create your views here.
class List(SelectRelatedMixin,ListView):
    model = models.EmployeeProfileInfo
    select_related = ('user',)
    queryset = model.objects.filter(user__is_active=True)
    # print(queryset)
    context_object_name = 'employee_list'
    template_name = 'employee/employee_list.html'

class EmployeeUpdateView(UpdateView):
    form_class = forms.EmployeeForm
    second_form_class = forms.EmployeeProfileInfoForm
    success_url = reverse_lazy("employee:list")
    template_name = 'employee/registration_form.html'

    def get_context_data(self, **kwargs):
        model = models.EmployeeProfileInfo
        queryset = model.objects.filter(user__pk=self.kwargs.get('pk'))
        instance = get_object_or_404(queryset)
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=instance)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=instance)
        return context

    def get_object(self):
        model = models.User
        return get_object_or_404(model.objects.select_related(),pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        registered = False
        model = models.EmployeeProfileInfo
        if request.method == 'POST':
            user_form = forms.EmployeeForm(data=request.POST)
            profile_form = forms.EmployeeProfileInfoForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                first_model = models.User.objects.get(pk=self.kwargs.get('pk'))

                second_model = get_object_or_404(model.objects.filter(user__pk=self.kwargs.get('pk')))

                first_model.first_name = request.POST['first_name']
                first_model.email = request.POST['email']
                first_model.save()
                if 'profile_pic' in request.FILES:
                    second_model.profile_pic = request.FILES['profile_pic']
                second_model.age = request.POST['age']
                second_model.phone = request.POST['phone']
                second_model.address = request.POST['address']

                second_model.save()
                registered = True
                return redirect('employee:list')
            else:
                print(user_form.errors,profile_form.errors)
        else:
            user_form = forms.EmployeeForm()
            profile_form = forms.EmployeeProfileInfoForm()

        return render(request,'employee/registration_form.html',
                                {'form':user_form,
                                'form2':profile_form,
                                'registered':registered})

class Registration(CreateView):
    form_class = forms.EmployeeForm
    second_form_class = forms.EmployeeProfileInfoForm
    success_url = reverse_lazy("employee:list")
    template_name = 'employee/registration_form.html'

    def get_context_data(self, **kwargs):
        context = super(Registration, self).get_context_data(**kwargs)
        print(context)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        registered = False
        def get_queryset(self):
            notifications = EmployeeProfileInfo.objects.all()
            return notifications

        def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        User._meta.get_field('email')._unique = True
        if request.method == 'POST':
            user_form = forms.EmployeeForm(data=request.POST)
            profile_form = forms.EmployeeProfileInfoForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.is_active = False
                user.username = user.first_name + '_' + random_generator()
                user.set_password(user.first_name + '_' + random_generator())
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']

                profile.save()
                registered = True

                current_site = get_current_site(request)
                subject = 'Activate Your MySite Account'
                message = render_to_string('employee/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': default_token_generator.make_token(user)
                    })
                user.email_user(subject, message)
                return redirect('home')
            else:
                print(user_form.errors,profile_form.errors)
        else:
            user_form = forms.EmployeeForm()
            profile_form = forms.EmployeeProfileInfoForm()

        return render(request,'employee/registration_form.html',
                                {'form':user_form,
                                'form2':profile_form,
                                'registered':registered})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'POST':

        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 == new_password2:
            user.set_password(new_password1)
            user.save()
            return render(request, 'employee/password_reset.html', {
                'validlink': True,
                'error_message': "Your password updated",
            })
        else:
            return render(request, 'employee/password_reset.html', {
                'validlink': True,
                'error_message': "Your both password not match",
            })
    else:
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            validlink = {'validlink':True}
            user.save()

            return render(request, 'employee/password_reset.html',context=validlink)
        else:
            return render(request, 'account_activation_invalid.html',{'validlink': False})
    return render(request, 'account_activation_invalid.html',{'validlink': False})

@login_required
def delete_employee(request,pk=None):
    if request.user.is_superuser:
        try:
            obj = get_object_or_404(models.User,pk=pk)
            obj.is_active = False
            obj.save()
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    return redirect('employee:list')

class EmployeeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)

def ajax_list(request):

    events = models.User.objects.filter(is_active=True)
    serializer = EmployeeSerializer(events, many=True)
    data = {
        'list': serializer.data
    }
    return JsonResponse(data)
