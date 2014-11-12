from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string


def use_template(request):
    rendered = render_to_string('simgtd/email/duedate.html', {'name': request.user.get_full_name()})
    return HttpResponse(rendered)
