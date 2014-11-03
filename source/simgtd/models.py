import datetime

from django.db import models
from django.contrib.auth.models import User, Group


class Constants(object):

    status_not_started = 1
    status_in_process = 2
    status_completed = 3
    status_suspended = 4

    priority_low = 1
    priority_normal = 2
    priority_high = 3

    user_admin = 1


class Status(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

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

    def __unicode__(self):
        return self.subject

    def time(self):
        ts = ''
        if self.hours > 0:
            ts = ts + str(self.hours) + ' hours'
        if self.minutes > 0:
            ts = ts + str(self.minutes) + ' minutes'

        return ts

    def done(self):
        if self.status_id == Constants.status_completed:
            return 'done'
        else:
            return 'in progress'


class LoginResult():
    def __init__(self, name, password):
        self.name = name
        self.password = password
