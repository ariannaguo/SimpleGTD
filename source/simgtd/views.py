import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from simgtd.models import login_result


@login_required
def say(request):
    says = []
    says.append('Do what you like and like what you are doing.')
    says.append(datetime.datetime.now())
    says.append('Greeting')

    return render_to_response('simgtd/says.html',
        RequestContext(request, {'says': says}))


@login_required
def about(request):
    return render_to_response('simgtd/about.html',
        RequestContext(request))


@login_required
def home(request):
    return render_to_response('simgtd/home.html',
        RequestContext(request))


def login(request):
    errors = []
    result = {}
    if request.method == 'POST':
        name = request.POST['name']
        pwd = request.POST['password']
        if name and pwd:
            user = auth.authenticate(username = name, password = pwd)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    next_page = '/'
                    if 'next' in request.GET:
                        next_page = request.GET['next']
                    return HttpResponseRedirect(next_page)
                else:
                    errors.append('this user is not in active status.')
            else:
                errors.append('please enter your valid name & password.')
        else:
            errors.append('please enter your name & password.')

        result = login_result(name, pwd)

    return render_to_response('simgtd/login.html',
            RequestContext(request, { 'errors': errors, 'result': result }))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
