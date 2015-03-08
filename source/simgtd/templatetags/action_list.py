import datetime
from django import template

register = template.Library()


@register.inclusion_tag('simgtd/tags/action_list.html', takes_context=True)
def action_list(context, actions, list_id):
    return {'actions': actions,
            'list_id': list_id,
            'STATIC_URL': context['STATIC_URL']}


@register.inclusion_tag('simgtd/tags/action_overdue.html', takes_context=True)
def action_overdue(context, actions, list_id):
    return {'actions': actions,
            'list_id': list_id,
            'STATIC_URL': context['STATIC_URL']}


# register.inclusion_tag('simgtd/tags/action_list.html')(action_list)