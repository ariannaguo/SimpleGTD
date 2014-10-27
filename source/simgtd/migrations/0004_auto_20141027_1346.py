# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('simgtd', '0003_auto_20141025_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='completed_date',
            field=models.DateTimeField(null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
            preserve_default=True,
        ),
    ]
