# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simgtd', '0007_auto_20141108_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='remind_sms',
            field=models.NullBooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='setting',
            name='remind_email',
            field=models.NullBooleanField(default=True),
        ),
    ]
