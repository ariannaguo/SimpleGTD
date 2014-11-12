from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils import timezone

from common import dt
from common.leancloud import send_due_notification, send_due_notification2
from simgtd import settings, gtd_settings
from simgtd.models import Goal, Constants


class Command(BaseCommand):
    help = 'Check due dates for goals and actions'

    def add_arguments(self, parser):
        parser.add_argument('max', nargs='?', type=int)

    def notify_email(self, user, goals):

        now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        overdue = [g for g in goals if g.due_date < now]
        will_be_due = [g for g in goals if g.due_date >= now]

        self.stdout.write(str(len(goals)))
        self.stdout.write(str(len(overdue)))
        self.stdout.write(str(len(will_be_due)))

        mail = render_to_string('simgtd/email/duedate.html',
                                {'name': user.first_name,
                                 'root': settings.SITE_ROOT,
                                 'goal_overdue': overdue,
                                 'goal_will_be_due': will_be_due})

        self.stdout.write(user.first_name)
        self.stdout.write(mail)
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
        due = now + timedelta(days=gtd_settings.notify_before_days)
        self.stdout.write(str(due))
        two_months_ago = dt.week_range(now, -8)
        due_goals = Goal.objects.filter(created_date__gt=two_months_ago[0],
                                        due_date__lt=due)\
                                .exclude(status_id=Constants.status_completed)

        user_goals = {}
        for g in due_goals:
            if g.created_by not in user_goals.keys():
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