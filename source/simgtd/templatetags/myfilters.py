from django import template

register = template.Library()


# @register.filter(name='cut2')
def cut2(value, arg):
    print(value)
    print(arg)
    print(value.replace(arg, ''))
    return value.replace(arg, '')


@register.filter
def lower2(value):
    return value.lower()


register.filter('cut2', cut2)
# register.filter('lower2', lower2)

