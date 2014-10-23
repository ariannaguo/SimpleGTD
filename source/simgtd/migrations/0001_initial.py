# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=200)),
                ('memo', models.TextField(max_length=1000, blank=True)),
                ('duration', models.PositiveIntegerField(blank=True)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('due_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('remind_me', models.NullBooleanField(default=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('completed_date', models.DateTimeField(null=True, editable=False)),
                ('progress', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='goal',
            name='priority',
            field=models.ForeignKey(default=2, to='simgtd.Priority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='status',
            field=models.ForeignKey(default=1, to='simgtd.Status'),
            preserve_default=True,
        ),
    ]
