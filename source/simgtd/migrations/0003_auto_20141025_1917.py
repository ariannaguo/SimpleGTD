# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simgtd', '0002_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='days',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='week_offset',
            field=models.PositiveSmallIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
