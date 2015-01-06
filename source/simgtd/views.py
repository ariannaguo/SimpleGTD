from datetime import datetime, timedelta
import json
import logging

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from taggit.models import Tag

from simgtd import settings, gtd_settings
from simgtd.models import Goal, Action, Constants, ActionComment, GoalComment
from common import dt


def make_tz_aware(d):
    return timezone.make_aware(d, timezone.get_default_timezone())


@login_required
def email(request):
    says = ['Do what you like and like what you are doing.', datetime.now(), 'Greeting']
    send_mail(says[0], 'message here', 'SimpleGTD <' + settings.EMAIL_ADMIN + '>', ['anderscui@gmail.com'],
              fail_silently=False)
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
        progress = request.POST['progress']
        status = request.POST['status']

        if subject and duration and due_date:
            goal = user_goals(request).get(id=gid)
            goal.subject = subject
            goal.duration = duration
            goal.due_date = datetime.strptime(due_date, '%m/%d/%Y')
            goal.progress = int(progress)
            goal.status_id = int(status)
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
    all_goals = user_goals(request).filter(created_by_id=user_id(request)) \
        .order_by('status_id', '-start_date')

    return render_to_response('simgtd/goal_list.html',
                              RequestContext(request, {'goals': all_goals}))


@login_required
@require_http_methods(['POST'])
def goal_status(request, gid):
    gid = int(gid)
    sid = int(request.POST['sid'])

    if sid in [1, 2, 3] and gid > 0:

        goal = user_goals(request).get(id=gid)

        if sid == Constants.status_in_process and goal.status_id != Constants.status_in_process:
            count = user_goals(request).filter(status_id=Constants.status_in_process).count()
            if count >= gtd_settings.max_goal_in_process:
                resp_data = {'gid': gid, 'result': 'ERROR',
                             'message': 'Exceeding the limit of {0}'.format(gtd_settings.max_goal_in_process)}
                return HttpResponse(json.dumps(resp_data), content_type="application/json")

        goal.status_id = sid
        goal.save()
        resp_data = {'gid': gid, 'result': 'OK'}

    else:
        resp_data = {'gid': gid, 'result': 'ERROR', 'message': 'Invalid arguments'}

    return HttpResponse(json.dumps(resp_data), content_type="application/json")


def match_day(action, week):
    week_start = make_tz_aware(week[0])
    week_end = make_tz_aware(week[1])
    return week_start <= action.start_date <= week_end


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
    next_week = dt.week_range(today, 1)

    actions_three_weeks = user_actions(request).filter(start_date__gt=last_week[0],
                                                       start_date__lt=next_week[1])

    this_week_start = make_tz_aware(this_week[0])
    next_week_start = make_tz_aware(next_week[0])

    today_weekday = today.weekday() + 1
    daily = [a for a in actions_three_weeks
             if str(today_weekday) in a.days and a.start_date < next_week_start and
             match_day(a, this_week)]
    daily.sort(key=lambda a: (a.status_id, a.days))

    weekly = [a for a in actions_three_weeks
              if a.start_date < next_week_start and match_day(a, this_week)]
    weekly.sort(key=lambda a: (a.status_id, a.days))

    next = [a for a in actions_three_weeks
            if a.start_date > this_week_start and match_day(a, next_week)]
    next.sort(key=lambda a: (a.status_id, a.days))

    # overdue actions
    overdue_point = make_tz_aware(dt.week_range(today, -gtd_settings.overdue_weeks)[0])
    overdue = user_actions(request).filter(start_date__gt=overdue_point,
                                           start_date__lt=next_week_start,
                                           due_date__lt=datetime.now())\
        .exclude(status_id=Constants.status_completed)

    all_goals = user_goals(request).filter(status_id=Constants.status_in_process).order_by('subject')
    return render_to_response('simgtd/action_list.html',
                              RequestContext(request, {'daily': daily,
                                                       'weekly': weekly,
                                                       'next_week': next,
                                                       'overdue': len(overdue),
                                                       'overdue_weeks': gtd_settings.overdue_weeks,
                                                       'goals': all_goals}))


@login_required
@require_http_methods(['POST'])
def action_update(request):
    aid = request.POST['action_id']
    subject = request.POST['action']
    hours = request.POST['hours']
    minutes = request.POST['minutes']
    due_date = request.POST['due_date']
    tags = request.POST['tags']

    if aid and subject:
        try:
            action_id = int(aid)
            is_new = action_id <= 0

            action = None
            if is_new:
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

            now = datetime.now()
            if is_new:
                action.created_date = now
                action.created_by = request.user
                action.start_date = now + timedelta(weeks=check_week)
            else:
                this_week = dt.week_range(datetime.now().today(), 0)
                week_offset = 0
                if action.start_date > make_tz_aware(this_week[1]):
                    week_offset = 1
                action.start_date = action.start_date + timedelta(weeks=(check_week-week_offset))

            action.save()

            action.tags.clear()
            for tag in tags.split(','):
                tag = tag.strip()
                if tag:
                    action.tags.add(tag)
            action.save()

            updated = {"id": action.id,
                       "status": action.status_id,
                       "subject": action.subject,
                       "days": action.days,
                       "time": action.time(),
                       "start_date": dt.to_standard_string(action.start_date),
                       "due_date": action.due_date.strftime("%b. %d (%a)")
                       }
            if action.goal:
                updated["goal"] = action.goal.subject

            resp_data = {"aid": action.id, "action": updated, 'result': 'OK', 'message': 'you got it!'}

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

    res = {}
    if action:
        # serializers are only used for django models.
        # resp_data = serializers.serialize('json', {'action': action, 'tags': ts})
        res['action'] = model_to_dict(action, exclude='tags')
        res['tags'] = action.tag_list()
        if action.goal:
            res["goal"] = action.goal.subject
    else:
        res = {"aid": 0, 'result': 'ERROR', 'message': 'Action not found'}

    return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def actions_of_tag(request, tag):
    actions = user_actions(request).filter(tags__name__in=[tag])
    return render_to_response('simgtd/actions_of_tag.html',
                              RequestContext(request, {'tag': tag, 'actions': actions}))


@login_required
def action_tags(request):
    tags = Tag.objects.filter(action__created_by=request.user).distinct()
    return render_to_response('simgtd/action_tags.html',
                              RequestContext(request, {'tags': tags}))


@login_required
def action_comments(request, aid):
    action = user_actions(request).get(id=int(aid))
    return render_to_response('simgtd/action_comments.html',
                              RequestContext(request, {'action': action}))


@login_required
def add_action_comment(request, aid):
    comment = request.POST['comment']
    if comment:
        ac = ActionComment(comment=comment, action_id=aid)
        ac.save()

    return HttpResponseRedirect('/action/list/')


@login_required
@require_http_methods(['POST'])
def action_status(request, aid):
    aid = int(aid)
    sid = int(request.POST['sid'])
    if sid in [1, 2, 3] and aid > 0:
        action = user_actions(request).get(id=aid)
        if action.status_id != Constants.status_completed and sid == Constants.status_completed:
            action.completed_date = datetime.now()
        action.status_id = sid
        action.save()

        updated = {"id": action.id,
                   "status": action.status_id,
                   "subject": action.subject,
                   "days": action.days,
                   "time": action.time(),
                   "start_date": dt.to_standard_string(action.start_date),
                   "due_date": action.due_date.strftime("%b %d (%a)")
                   }
        if action.goal:
            updated["goal"] = action.goal.subject

        resp_data = {"aid": action.id, "action": updated, 'result': 'OK', 'message': 'you got it!'}
    else:
        resp_data = {'aid': aid, 'result': 'ERROR'}

    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@login_required
def overdue(request):
    overdue_actions = user_actions(request).filter(due_date__lt=datetime.now())\
                                           .exclude(status_id=Constants.status_completed)

    today = datetime.today()
    overdue_point = make_tz_aware(dt.week_range(today, -gtd_settings.overdue_weeks)[0])
    recent = [a for a in overdue_actions if a.due_date > overdue_point]
    recent.sort(key=lambda a: a.due_date, reverse=True)

    earlier = [a for a in overdue_actions if a.due_date <= overdue_point]
    earlier.sort(key=lambda a: a.due_date, reverse=True)

    return render_to_response('simgtd/action_overdue.html',
                              RequestContext(request, {'recent': recent,
                                                       'earlier': earlier,
                                                       'total': len(overdue_actions)}))