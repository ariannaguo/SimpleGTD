from datetime import datetime
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils import translation

from common import dt
from common.leancloud import send_due_notification, send_due_notification2
from simgtd import settings
from simgtd.models import Goal, Constants


class Command(BaseCommand):
    help = 'Check due dates for goals and actions'

    def add_arguments(self, parser):
        parser.add_argument('max', nargs='?', type=int)

    def notify_email(self, user, goals):
        mail = render_to_string('simgtd/email/duedate.html',
                                {'name': user.first_name, 'goal_will_be_due': goals})
        self.stdout.write(user.first_name)
        send_mail('Overdue Goals', '',
                  'SimpleGTD <' + settings.EMAIL_ADMIN + '>',
                  [user.email],
                  html_message=mail,
                  fail_silently=False)

    def notify_sms(self, user, goals):
        # TODO: send sms to user
        sms = ''

    def handle(self, *args, **options):
        # translation.activate('zh-cn')

        now = datetime.now()
        two_months_ago = dt.week_range(now, -8)
        this_week = dt.week_range(now, 0)
        due_goals = Goal.objects.filter(created_date__gt=two_months_ago[0],
                                        created_date__lt=this_week[1],
                                        status_id=Constants.status_in_process,
                                        due_date__lt=now)

        user_goals = {}
        for g in due_goals:
            if g.created_by_id not in user_goals.keys():
                user_goals[g.created_by] = []
            user_goals[g.created_by].append(g)

        # for g in due_goals:
        # self.stdout.write('sending sms')
        #     #self.stdout.write(now.strftime("%B %d, %Y"))
        #     #send_due_notification(anders, 'duedate', 'goal', g.subject, now.strftime("%b %d"), 'http://simplegtd.me/')
        #     #send_due_notification2(anders, 'duedate', 'goal', g.subject,
        #     #                       g.due_date.strftime("%b %d, %A"), 'http://simplegtd.me/goal/list')
        #     self.stdout.write('sms sent')
        #
        #     self.stdout.write('Goal "%s"' % g.subject)
        #     # translation.deactivate()

        for user in user_goals.keys():
            self.notify_email(user, user_goals[user])