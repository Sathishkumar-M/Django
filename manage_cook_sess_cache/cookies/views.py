import datetime

from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext

from django.contrib.auth.forms import AuthenticationForm


def login(request):
    username = "not logged in"

    if request.method == "POST":
        print(request.POST['username'])
        if request.POST['username']:
            username = request.POST['username']

    response = render(request, "cookies/loggedin.html", {"username": username})

    response.set_cookie('last_connection', datetime.datetime.now())
    response.set_cookie('username', username)

    return response


def formView(request):

    if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        username = request.COOKIES['username']

        last_connection = request.COOKIES['last_connection']
        last_connection_time = datetime.datetime.strptime(last_connection[:-7],
                                                          "%Y-%m-%d %H:%M:%S")

        if (datetime.datetime.now() - last_connection_time).seconds < 10:
            return render(request, 'cookies/loggedin.html', {"username": username})
        else:
            return render(request, 'cookies/login.html', {'form':AuthenticationForm})

    else:
        return render(request, 'cookies/login.html', {'form':AuthenticationForm})