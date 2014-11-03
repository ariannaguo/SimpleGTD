from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from simgtd.models import LoginResult


def login(request):
    errors = []
    result = {}
    if request.method == 'POST':
        name = request.POST['name']
        pwd = request.POST['password']
        if name and pwd:
            user = auth.authenticate(username=name, password=pwd)
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

        result = LoginResult(name, pwd)

    return render_to_response('simgtd/login.html',
                              RequestContext(request, {'errors': errors, 'result': result}))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

