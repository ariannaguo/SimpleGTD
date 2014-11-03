from datetime import datetime, timedelta
import json
import logging

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from simgtd.models import Goal, Action
from common import dt


@login_required
def say(request):
    says = ['Do what you like and like what you are doing.', datetime.now(), 'Greeting']
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
            goal.created_by = request.user
            goal.save()

            return HttpResponseRedirect('/goal/list')
        else:
            errors.append('incomplete data')

    return render_to_response('simgtd/add_goal.html', RequestContext(request))


@login_required
def edit_goal(request, gid):
    errors = []

    goal = None
    if request.method == 'POST':

        subject = request.POST['title']
        duration = request.POST['duration']
        due_date = request.POST['due_date']

        if subject and duration and due_date:
            goal = user_goals(request).get(id=gid)
            goal.subject = subject
            goal.duration = duration
            goal.due_date = datetime.strptime(due_date, '%m/%d/%Y')
            goal.save()

            return HttpResponseRedirect('/goal/list')
        else:
            errors.append('incomplete data')
    else:
        goal = get_object_or_404(user_goals(request), id=gid)

    return render_to_response('simgtd/edit_goal.html',
                              RequestContext(request, {'goal': goal}))


@login_required
def goals(request):
    all_goals = user_goals(request).filter(created_by_id=user_id(request))\
                                   .order_by('-start_date')

    return render_to_response('simgtd/goal_list.html',
                              RequestContext(request, {'goals': all_goals}))


def match_day(action, point):
    return (action.created_date < point and action.week_offset == 1) \
           or (action.created_date > point and action.week_offset == 0)


def user_id(request):
    return request.user.id


def user_actions(request):
    return Action.objects.filter(created_by_id=user_id(request))


def user_goals(request):
    return Goal.objects.filter(created_by_id=user_id(request))


@login_required
def action_list(request):
    today = datetime.today()
    last_week = dt.week_range(today, -1)
    this_week = dt.week_range(today, 0)

    actions_two_weeks = user_actions(request).filter(created_date__gt=last_week[0],
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

    all_goals = user_goals(request).order_by('-start_date')
    return render_to_response('simgtd/action_list.html',
                              RequestContext(request, {"daily": daily, 'weekly': weekly, 'goals': all_goals}))


@login_required
@require_http_methods(['POST'])
def action_update(request):

    aid = request.POST['action_id']
    subject = request.POST['action']
    hours = request.POST['hours']
    minutes = request.POST['minutes']
    due_date = request.POST['due_date']

    if aid and subject:
        try:
            action_id = int(aid)

            action = None
            if action_id <= 0:
                action = Action()
            else:
                action = user_actions(request).get(id=aid)

            action.subject = subject

            if hours:
                action.hours = int(hours)
            else:
                action.hours = 0

            if minutes:
                action.minutes = int(minutes)
            else:
                action.minutes = 0

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

            if action_id <= 0:
                action.created_date = datetime.now()
                action.created_by = request.user

            action.save()

            resp_data = {"aid": action.id, 'result': 'OK', 'message': 'you got it!'}

        except Exception as e:
            print(e.message)
            logging.error(e)
            resp_data = {"aid": 0, 'result': 'ERROR', 'message': 'server error'}
    else:
        resp_data = {"aid": 0, 'result': 'ERROR', 'message': 'incomplete data'}

    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@login_required
def action_get(request, aid):
    action = user_actions(request).get(id=int(aid))

    if action:
        resp_data = serializers.serialize('json', [action])
        #resp_data = {"aid": int(aid), 'actions': resp_data, 'result': 'OK'}
    else:
        resp_data = {"aid": 0, 'result': 'ERROR', 'message': 'Action not found'}

    return HttpResponse(resp_data, content_type="application/json")
    #return JsonResponse(resp_data, safe=False)

