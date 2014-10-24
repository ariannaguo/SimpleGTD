from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from simgtd.models import login_result, Goal, Constants


@login_required
def say(request):
    says = []
    says.append('Do what you like and like what you are doing.')
    says.append(datetime.now())
    says.append('Greeting')

    return render_to_response('simgtd/says.html', RequestContext(request, {'says': says}))


@login_required
def about(request):
    return render_to_response('simgtd/about.html', RequestContext(request))


@login_required
def home(request):
    return render_to_response('simgtd/home.html', RequestContext(request))


@login_required
def add_goal(request):

    errors = []
    result = {}

    if request.method == 'POST':
        subject = request.POST['title']
        duration = request.POST['duration']
        due_date = request.POST['due_date']

        if subject and duration and due_date:
            goal = Goal()
            goal.subject = subject
            goal.duration = duration
            goal.due_date = datetime.strptime(due_date, '%m/%d/%Y')
            goal.created_date = datetime.now()
            goal.save()

            return HttpResponseRedirect('/goal/list')
        else:
            errors.append('incomplete data')

    return render_to_response('simgtd/add_goal.html', RequestContext(request))


@login_required
def edit_goal(request, gid):

    errors = []
    result = {}

    if request.method == 'POST':

        subject = request.POST['title']
        duration = request.POST['duration']
        due_date = request.POST['due_date']

        if subject and duration and due_date:
            goal = Goal.objects.get(id=gid)
            goal.subject = subject
            goal.duration = duration
            goal.due_date = datetime.strptime(due_date, '%m/%d/%Y')
            goal.save()

            return HttpResponseRedirect('/goal/list')
        else:
            errors.append('incomplete data')
    else:

        goal = Goal.objects.get(id=gid)

    return render_to_response('simgtd/edit_goal.html',
                              RequestContext(request, {'goal': goal}))


@login_required
def goals(request):
    all_goals = Goal.objects.order_by('-start_date')

    return render_to_response('simgtd/goal_list.html',
                              RequestContext(request, {'goals': all_goals}))


@login_required
def action_list(request):
    return render_to_response('simgtd/action_list.html', RequestContext(request))


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

        result = login_result(name, pwd)

    return render_to_response('simgtd/login.html',
                              RequestContext(request, {'errors': errors, 'result': result}))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


