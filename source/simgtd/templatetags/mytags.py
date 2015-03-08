import datetime
from django import template

register = template.Library()


class CurrentTimeNode(template.Node):
    def __init__(self, format_str):
        self.format_str = format_str

    def render(self, context):
        return datetime.datetime.now().strftime(self.format_str)


class FormatTimeNode(template.Node):
    def __init__(self, to_be_formatted, format_str):
        self.to_be_formatted = template.Variable(to_be_formatted)
        self.format_str = format_str

    def render(self, context):
        try:
            actual = self.to_be_formatted.resolve(context)
            return actual.strftime(self.format_str)
        except template.VariableDoesNotExist:
            return 'invalid'


@register.tag()
def cur_time(parser, token):
    try:
        tag_name, format_str = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )

    if not (format_str[0] == format_str[-1] and format_str[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )

    return CurrentTimeNode(format_str[1:-1])


@register.tag()
def fmt_time(parser, token):
    try:
        tag_name, to_be_formatted, format_str = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )

    if not (format_str[0] == format_str[-1] and format_str[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )

    return FormatTimeNode(to_be_formatted, format_str[1:-1])


# using simple tags
@register.simple_tag()
def cur_time2(format_str):
    return datetime.datetime.now().strftime(format_str)