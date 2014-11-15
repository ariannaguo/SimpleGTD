# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simgtd', '0010_auto_20141113_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=500, blank=True)),
                ('html', models.TextField(max_length=1000, editable=False, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('created_by', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
                ('goal', models.ForeignKey(related_name=b'comments', to='simgtd.Goal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
