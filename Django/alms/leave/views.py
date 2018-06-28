from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponseForbidden,Http404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from employee.tokens import account_activation_token

from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMessage
from django.http import HttpResponse
import string
from django.http import JsonResponse
from django.db.models import Count

# Create your views here.
class List(LoginRequiredMixin,ListView):
    model = models.LeaveRules
    template_name = 'leave/leave_rules_list.html'

class LeaveRulesDeleteView(DeleteView):
    model = models.LeaveRules
    success_url = reverse_lazy("leave:list")

class LeaveRulesCreateView(LoginRequiredMixin,CreateView):
    form_class = forms.LeaveRulesForm
    template_name = 'leave/leave_rules_form.html'
    success_url = reverse_lazy("leave:list")

class LeaveRulesDetail(LoginRequiredMixin,DetailView):
    model = models.LeaveRules
    template_name = 'leave/leave_rules_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk__iexact=self.kwargs.get('pk'))

class LeaveRulesUpdateView(LoginRequiredMixin,UpdateView):
    model = models.LeaveRules
    fields = ('leave_type','leave_rules')
    template_name = 'leave/leave_rules_form.html'
    # success_url = reverse_lazy("leave:detail" pk=leaverules.pk)
    success_url = reverse_lazy("leave:list")

class LeaveApplyCreateView(LoginRequiredMixin,CreateView):
    form_class = forms.LeaveApplyForm
    template_name = 'leave/leave_apply_form.html'
    success_url = reverse_lazy("leave:list")

    def post(self, request, *args, **kwargs):
        registered = False

        if request.method == 'POST':
            leave_form = forms.LeaveApplyForm(data=request.POST)
            draft = request.POST.get('save', False)

            if leave_form.is_valid():
                leave = leave_form.save(commit=False)
                leave.user = request.user
                flag = 1
                if draft != 'Save':
                    leave.published_date = timezone.now()
                    leave.save()
                    flag = leave_send_mails(request,leave.id)
                else:
                    leave.save()
                registered = True
                if flag != 1:
                    return redirect('leave:applied')
                else:
                    return redirect('leave:draft', username=request.user.username)

            else:
                print(leave_form.errors)
        else:
            leave_form = self.form_class

        return render(request,self.template_name,
                                {'form':leave_form,
                                'registered':registered})

class LeaveAppliedListView(LoginRequiredMixin,ListView,BaseException):
    model = models.LeaveApply
    template_name = 'leave/leave_apply_status_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        else:
            raise Http404()

class LeaveAppliedUserListView(LoginRequiredMixin,ListView,BaseException):
    model = models.LeaveApply
    template_name = 'leave/leave_apply_list.html'

    def get_queryset(self):
        if self.kwargs.get('username') == self.request.user.username:
            return self.model.objects.filter(user__username__iexact=self.kwargs.get('username'),published_date__lte=timezone.now()).order_by('-published_date')
        else:
            raise Http404()

class LeaveDraftListView(LoginRequiredMixin,ListView,BaseException):
    model = models.LeaveApply
    template_name = 'leave/leave_apply_list.html'

    def get_queryset(self):
        if self.kwargs.get('username') == self.request.user.username:
            return self.model.objects.filter(user__username__iexact=self.kwargs.get('username'),published_date__isnull=True).order_by('created_date')
        else:
            raise Http404()

class LeaveApplyUpdateView(LoginRequiredMixin,UpdateView):
    model = models.LeaveApply
    fields = ('leave_type','start_date','end_date','notes','tag_to')
    template_name = 'leave/leave_apply_form.html'
    # success_url = reverse_lazy("leave:detail" pk=leaverules.pk)
    success_url = reverse_lazy("leave:applied")

class LeaveApplyDeleteView(LoginRequiredMixin,DeleteView):
    model = models.LeaveApply
    success_url = reverse_lazy("leave:applied")

def leave_send_mails(request,leave_id):
    model = models.LeaveApply
    start_date = datetime.strptime(request.POST['start_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
    end_date = datetime.strptime(request.POST['end_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
    user_leave_history = model.objects.filter(user__username__iexact=request.user.username,published_date__lte=timezone.now()).exclude(pk=leave_id). extra(select={\
        'month': "EXTRACT(month FROM published_date)",
        'year': "EXTRACT(year FROM published_date)",
    }).\
    values('month', 'year').\
    annotate(count_items=Count('published_date')).order_by('-published_date')
    print ("month,count,total")
    total = 0
    for item in user_leave_history:
        total = total + item['count_items']
        if item['year'] < 2018: continue
        print ("%02d-%s,%s,%s" % (item['month'], item['year'], item['count_items'], total))
    others_leave_history = model.objects.filter(published_date__range=(start_date, end_date)).exclude(user__username__iexact=request.user.username).order_by('-published_date')
    superusers = models.User.objects.filter(is_superuser=True)
    recipient_list = request.POST['tag_to']
    for suser in superusers:
        if suser.email not in recipient_list:
            if request.user.email not in suser.email:
                recipient_list += suser.email

    recipient_list = list(set(recipient_list.split(",")))

    current_site = get_current_site(request)
    subject = 'Leave request'

    for rlist in recipient_list:
        if rlist.strip():
            message = render_to_string('leave/leave_request_email.html', {
                'domain': current_site.domain,
                'user': request.user,
                'leave_details': request.POST,
                'user_history': user_leave_history,
                'other_history': others_leave_history,
                'Approved': urlsafe_base64_encode(force_bytes('Approved')).decode(),
                'Declined': urlsafe_base64_encode(force_bytes('Declined')).decode(),
                'uidb64': urlsafe_base64_encode(force_bytes(request.user.pk)).decode(),
                'lidb64': urlsafe_base64_encode(force_bytes(leave_id)).decode(),
                'approve_by': urlsafe_base64_encode(force_bytes(rlist)).decode(),
                'token': default_token_generator.make_token(request.user)
                })
            print(message)
            email = EmailMessage(subject, message, "sathishkumar@appinessworld.com", [rlist])
            email.content_subtype = "html"
            res = email.send()
            return HttpResponse('%s'%res)

def status(request,status,approve_by, uidb64, lidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None
    try:
        lid = force_text(urlsafe_base64_decode(lidb64))
        leave = models.LeaveApply.objects.get(pk=lid)
    except (TypeError, ValueError, OverflowError, models.LeaveApply.DoesNotExist):
        leave = None
    if user and default_token_generator.check_token(user, token):
        status = force_text(urlsafe_base64_decode(status))
        approved_email = force_text(urlsafe_base64_decode(approve_by))
        status_by = models.User.objects.get(email=approved_email)

        leave.status = status
        leave.status_by = status_by.first_name
        leave.save()
        flag = leave_status_mails(request,user,leave,approved_email)
        validlink = {'validlink':True}
        return render(request, 'leave/leave_status.html',context=validlink)
    else:
        return render(request, 'leave/leave_status.html',{'validlink': False})

def leave_status_mails(request,user,leave,approved_email):
    superusers = models.User.objects.filter(is_superuser=True)
    recipient_list = leave.tag_to
    for suser in superusers:
        if suser.email not in recipient_list:
            if user.email not in suser.email:
                recipient_list += suser.email

    recipient_list += user.email

    recipient_list = list(set(recipient_list.split(",")))

    current_site = get_current_site(request)
    subject = 'Leave status'

    for rlist in recipient_list:
        if rlist.strip():
            if rlist not in approved_email:
                message = render_to_string('leave/leave_status_email.html', {
                    'domain': current_site.domain,
                    'user': user,
                    'leave_details': leave,
                    })
                print(message)
                email = EmailMessage(subject, message, "sathishkumar@appinessworld.com", [rlist])
                email.content_subtype = "html"
                res = email.send()
                return HttpResponse('%s'%res)

def leave_status(request):
    approved_email = request.GET.get('approved_email')
    data = request.GET.get('data').split(",")
    try:
        user_id = data[2]
        user = models.User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None
    try:
        leave_id = data[1]
        leave = models.LeaveApply.objects.get(pk=leave_id)
    except (TypeError, ValueError, OverflowError, models.LeaveApply.DoesNotExist):
        leave = None

    if user and leave:
        status = data[0]
        status_by = models.User.objects.get(email=approved_email)

        leave.status = status
        leave.status_by = status_by.first_name
        leave.save()
        flag = leave_status_mails(request,user,leave,approved_email)
        updated = True
    else:
        updated = False
    data = {
        'is_taken': updated
    }
    return JsonResponse(data)
