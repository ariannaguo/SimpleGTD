import datetime

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from taggit.managers import TaggableManager
from common import dt


class Constants(object):

    status_not_started = 1
    status_in_process = 2
    status_completed = 3
    status_suspended = 4
    status_canceled = 5

    priority_low = 1
    priority_normal = 2
    priority_high = 3

    user_admin = 1


class Status(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

    @classmethod
    def active_list(cls):
        return [Constants.status_not_started,
                Constants.status_in_process,
                Constants.status_completed]

    @classmethod
    def inactive_list(cls):
        return [Constants.status_suspended,
                Constants.status_canceled]

    @classmethod
    def all(cls):
        return Status.active_list() + Status.inactive_list()

    def __unicode__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name


class Goal(models.Model):
    subject = models.CharField(max_length=200)
    memo = models.TextField(max_length=1000, blank=True)
    duration = models.PositiveIntegerField(blank=True)
    start_date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    due_date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    remind_me = models.NullBooleanField(default=True, null=True, blank=True)
    created_date = models.DateTimeField(editable=False, default=datetime.datetime.now)
    completed_date = models.DateTimeField(editable=False, null=True)

    created_by = models.ForeignKey(User, default=Constants.user_admin)

    progress = models.PositiveSmallIntegerField(default=0)
    status = models.ForeignKey(Status, default=Constants.status_not_started)
    priority = models.ForeignKey(Priority, default=Constants.priority_normal)

    def __unicode__(self):
        return self.subject

    def overdue(self):
        now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        return (self.status_id != Constants.status_completed) and (self.due_date < now)


class Action(models.Model):
    subject = models.CharField(max_length=200)
    memo = models.TextField(max_length=1000, blank=True)
    hours = models.PositiveSmallIntegerField(default=0)
    minutes = models.PositiveSmallIntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(editable=False, default=datetime.datetime.now)
    created_by = models.ForeignKey(User, default=Constants.user_admin)

    completed_date = models.DateTimeField(editable=False, null=True)

    week_offset = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    days = models.CharField(max_length=50, null=True, blank=True)

    status = models.ForeignKey(Status, default=Constants.status_not_started)

    goal = models.ForeignKey(Goal, null=True, blank=True)

    tags = TaggableManager(blank=True)

    def tag_list(self):
        ts = []
        for tag in self.tags.get_query_set():
            ts.append(tag.name)
        return ts

    def __unicode__(self):
        return self.subject

    def time(self):
        ts = ''
        if self.hours > 0:
            ts = ts + str(self.hours) + 'h'
        if self.minutes > 0:
            ts = ts + " " + str(self.minutes) + 'm'

        return ts

    def done(self):
        if self.status_id == Constants.status_completed:
            return 'done'
        else:
            return 'in progress'

    def overdue(self):
        now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        return (self.status_id != Constants.status_completed) and (self.due_date < now)


class ActionComment(models.Model):

    action = models.ForeignKey(Action, related_name='comments')
    comment = models.TextField(max_length=500, blank=True)
    html = models.TextField(max_length=1000, editable=False, blank=True)

    created_by = models.ForeignKey(User, default=Constants.user_admin)
    created_date = models.DateTimeField(editable=False, default=datetime.datetime.now)

    def __unicode__(self):
        return '{0} - {1}'.format(self.action, self.comment)


class GoalComment(models.Model):

    goal = models.ForeignKey(Goal, related_name='comments')
    comment = models.TextField(max_length=500, blank=True)
    html = models.TextField(max_length=1000, editable=False, blank=True)

    created_by = models.ForeignKey(User, default=Constants.user_admin)
    created_date = models.DateTimeField(editable=False, default=datetime.datetime.now)

    def __unicode__(self):
        return '{0} - {1}'.format(self.goal, self.comment)


class Setting(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    mobile_phone = models.CharField(max_length=20, null=True, blank=True)

    remind_sms = models.NullBooleanField(default=True, blank=True)
    remind_email = models.NullBooleanField(default=True, blank=True)

    remind_goal = models.NullBooleanField(default=True, blank=True)
    remind_action = models.NullBooleanField(default=False, blank=True)

    site_url = models.URLField(null=True)

    def __unicode__(self):
        return self.user.get_full_name()


class LoginResult():
    def __init__(self, name, password):
        self.name = name
        self.password = password
