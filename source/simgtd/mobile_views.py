from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string


def send_sms(request):
    return render_to_response('simgtd/sms.html', RequestContext(request))