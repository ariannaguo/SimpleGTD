# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simgtd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=200)),
                ('memo', models.TextField(max_length=1000, blank=True)),
                ('hours', models.PositiveSmallIntegerField(default=0)),
                ('minutes', models.PositiveSmallIntegerField(default=0)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('due_date', models.DateTimeField(null=True, blank=True)),
                ('goal', models.ForeignKey(blank=True, to='simgtd.Goal', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
