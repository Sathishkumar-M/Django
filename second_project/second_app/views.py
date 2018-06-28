from django.shortcuts import render
from second_app.models import User
# from . import forms
from second_app.forms import NameForm
# Create your views here.

def user(request):
    acc_data = User.objects.all()
    user_dict = {'user':acc_data}
    return render(request,'second_app/index.html',context=user_dict)

def formName(request):
    form = NameForm();

    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            print('From submitted!')
            form.save(commit=True)
            return user(request)
            # print('name: '+form.cleaned_data['name'])
            # print('Email: '+form.cleaned_data['email'])
            # print('Text: '+form.cleaned_data['text'])
        else:
            print('Error!')

    return render(request,'second_app/first_form.html',{'form': form})
