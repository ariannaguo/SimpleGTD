from django.shortcuts import render_to_response
from django.template import RequestContext


def send_sms(request):
    return render_to_response('simgtd/sms.html', RequestContext(request))



