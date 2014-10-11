import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def say(request):
    says = []
    says.append('Do what you like and like what you are doing.')
    says.append(datetime.datetime.now())
    says.append('Greeting')

    return render_to_response('simgtd/says.html',
        RequestContext(request, {'says': says}))


def about(request):
    return render_to_response('simgtd/about.html',
        RequestContext(request))


def home(request):
    return render_to_response('simgtd/home.html',
        RequestContext(request))
