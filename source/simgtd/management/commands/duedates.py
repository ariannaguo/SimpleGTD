from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils import timezone

from common import dt
from common.leancloud import send_due_notification, send_due_notification2
from simgtd import settings, gtd_settings
from simgtd.models import Goal, Constants, Action
from simgtd.views import overdue


class UserActions():

    overdue = None
    today = None

    def __init__(self):
        self.overdue = []
        self.today = []


class Command(BaseCommand):
    help = 'Check due dates for goals and actions'

    def add_arguments(self, parser):
        parser.add_argument('max', nargs='?', type=int)

    def notify_email(self, user, actions):

        actions_overdue = actions.overdue
        actions_today = actions.today

        self.stdout.write(str(len(actions_overdue)))
        self.stdout.write(str(len(actions_today)))

        mail = render_to_string('simgtd/email/duedate.html',
                                {'name': user.first_name,
                                 'root': settings.SITE_ROOT,
                                 'actions_overdue': actions_overdue,
                                 'actions_today': actions_today})

        self.stdout.write(user.first_name)
        self.stdout.write(mail)
        send_mail('Overdue Actions', '',
                  'SimpleGTD <' + settings.EMAIL_ADMIN + '>',
                  [user.email],
                  html_message=mail,
                  fail_silently=False)

    def notify_sms(user, goals):
        # TODO: send sms to user
        sms = ''

    def handle(self, *args, **options):
        # translation.activate('zh-cn')

        now = datetime.now()
        due = now
        self.stdout.write("due date time: " + str(due))
        two_months_ago = dt.week_range(now, -8)
        due_actions = Action.objects.filter(start_date__gt=two_months_ago[0],
                                            due_date__lt=due) \
            .exclude(status_id=Constants.status_completed)

        user_actions = {}
        for action in due_actions:
            if action.created_by not in user_actions.keys():
                user_actions[action.created_by] = UserActions()
            user_actions[action.created_by].overdue.append(action)

        this_week = dt.week_range(now, 0)
        actions_this_week = Action.objects.filter(start_date__gt=this_week[0], start_date__lt=this_week[1])
        today_weekday = str(now.weekday() + 1)
        today = [a for a in actions_this_week if today_weekday in a.days]

        for action in today:
            if action.created_by not in user_actions.keys():
                user_actions[action.created_by] = UserActions()
            user_actions[action.created_by].today.append(action)

        self.stdout.write(str(len(user_actions.keys())))

        for u in user_actions.keys():
            self.notify_email(u, user_actions[u])


