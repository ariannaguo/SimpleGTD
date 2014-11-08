# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simgtd', '0006_action_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=500, blank=True)),
                ('html', models.TextField(max_length=1000, editable=False, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('action', models.ForeignKey(to='simgtd.Action')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mobile_phone', models.TextField(max_length=20, null=True, blank=True)),
                ('remind_email', models.EmailField(max_length=75, null=True, blank=True)),
                ('remind_goal', models.NullBooleanField(default=True)),
                ('remind_action', models.NullBooleanField(default=False)),
                ('site_url', models.URLField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='actioncomment',
            name='created_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
