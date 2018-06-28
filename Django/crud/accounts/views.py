from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from accounts.models import User,UserProfileInfo
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from . import forms
# Create your views here.
class SignUp(CreateView):
    # form_class = {'user':forms.UserForm,'profile':forms.UserProfileInfoForm}
    form_class = forms.UserForm
    second_form_class = forms.UserProfileInfoForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/siginup_form.html'

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        registered = False
        def get_queryset(self):
            notifications = UserProfileInfo.objects.all()
            return notifications
        if request.method == 'POST':
            user_form = forms.UserForm(data=request.POST)
            profile_form = forms.UserProfileInfoForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']

                profile.save()
                registered = True
                # return render(request, 'accounts/login_form.html')
                return HttpResponseRedirect(self.get_success_url())
            else:
                print(user_form.errors,profile_form.errors)
        else:
            user_form = forms.UserForm()
            profile_form = forms.UserProfileInfoForm()

        # return self.get_context_data(**kwargs)

        return render(request,'accounts/siginup_form.html',
                                {'form':user_form,
                                'form2':profile_form,
                                'registered':registered})
        # return HttpResponseRedirect(self.get_success_url())
