from datetime import datetime, timedelta

import json
import logging

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from simgtd.models import login_result, Goal, Action

from common import dt


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

    goal = None
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


def match_day(action, point):
    return (action.created_date < point and action.week_offset == 1) \
           or (action.created_date > point and action.week_offset == 0)


@login_required
def action_list(request):
    today = datetime.today()
    last_week = dt.week_range(today, -1)
    this_week = dt.week_range(today, 0)

    actions_two_weeks = Action.objects.filter(created_date__gt=last_week[0],
                                              created_date__lt=this_week[1])

    today_start = today.date()
    today_end = today_start + timedelta(days=1)
    today_weekday = today.weekday() + 1
    daily = [a for a in actions_two_weeks
             if str(today_weekday) in a.days and
             match_day(a,
                       timezone.make_aware(this_week[0], timezone.get_default_timezone()))]

    weekly = [a for a in actions_two_weeks
              if match_day(a, timezone.make_aware(this_week[0], timezone.get_default_timezone()))]

    all_goals = Goal.objects.order_by('-start_date')
    return render_to_response('simgtd/action_list.html',
                              RequestContext(request, {"daily": daily, 'weekly': weekly, 'goals': all_goals}))


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


# @login_required
# def actions_today(request):



@login_required
def action_add(request):
    errors = []
    result = {}

    if request.method == 'POST':
        subject = request.POST['action']
        hours = request.POST['hours']
        minutes = request.POST['minutes']
        due_date = request.POST['due_date']

        if subject:
            action = Action()
            action.subject = subject

            if hours:
                action.hours = int(hours)

            if minutes:
                action.hours = int(minutes)

            if due_date:
                action.due_date = datetime.strptime(due_date, '%m/%d/%Y')

            check_week = int(request.POST['check_week'])
            if request.POST['check_day']:
                check_day = request.POST.getlist('check_day')
                action.days = ','.join([s.encode('ascii', 'ignore') for s in check_day])

            if request.POST['goal']:
                action.goal_id = int(request.POST['goal'])

            action.created_date = datetime.now()
            action.save()

            return HttpResponseRedirect('/action/list')

        else:
            errors.append('incomplete data')

    all_goals = Goal.objects.order_by('-start_date')
    return render_to_response('simgtd/add_action.html',
                              RequestContext(request, {'goals': all_goals}))


@login_required
@require_http_methods(['POST'])
def action_create(request):
    subject = request.POST['action']
    hours = request.POST['hours']
    minutes = request.POST['minutes']
    due_date = request.POST['due_date']

    if subject:
        try:
            action = Action()
            action.subject = subject

            if hours:
                action.hours = int(hours)

            if minutes:
                action.hours = int(minutes)

            if due_date:
                action.due_date = datetime.strptime(due_date, '%m/%d/%Y')

            check_week = int(request.POST['check_week'])
            action.week_offset = check_week

            if request.POST['check_day']:
                check_day = request.POST.getlist('check_day')
                action.days = ','.join([s.encode('ascii', 'ignore') for s in check_day])
                logging.info(','.join([s.encode('ascii', 'ignore') for s in check_day]))

            goal_id = request.POST.get('goal', '0')
            if goal_id:
                action.goal_id = int(goal_id)

            action.created_date = datetime.now()

            action.save()

            resp_data = {"aid": action.id, 'result': 'OK', 'message': 'you got it!'}

        except Exception as e:
            print(e.message)
            logging.error(e)
            resp_data = {"aid": 0, 'result': 'ERROR', 'message': 'server error'}
    else:
        resp_data = {"aid": 0, 'result': 'ERROR', 'message': 'incomplete data'}

    return HttpResponse(json.dumps(resp_data), content_type="application/json")



from django.core import serializers

@login_required
def action_get(request, aid):
    action = Action.objects.get(id=int(aid))

    if action:
        json_data = serializers.serialize('json', [action])
        resp_data = json_data
        #resp_data = {"aid": int(aid), 'actions': json_data, 'result': 'OK'}
    else:
        resp_data = {"aid": 0, 'result': 'ERROR', 'message': 'Action not found'}

    return HttpResponse(json.dumps(resp_data), content_type="application/json")