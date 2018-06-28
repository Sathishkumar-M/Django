from django.shortcuts import render
from django.http import HttpResponse
from AppTwo.models import User

# Create your views here.
def index(request):
    return HttpResponse('<em>my Second App</>')

def user(request):
    acc_data = User.objects.all()
    my_dict = {'accesusers': acc_data}
    return render(request,'appTwo/index.html',context=my_dict)
