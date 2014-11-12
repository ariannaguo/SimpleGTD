from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.leancloud import send_due_notification2


@login_required
def profile(request):
    return render_to_response('simgtd/me.html', RequestContext(request))


@login_required
def sms(request):
    if request.method == 'POST':
        msg = request.POST['msg']
        send_due_notification2('13482010377', 'duedate', 'goal', msg,
                               '', 'http://simplegtd.me/goal/list')

    return render_to_response('simgtd/sms.html', RequestContext(request))

