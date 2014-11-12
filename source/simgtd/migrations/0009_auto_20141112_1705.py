# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simgtd', '0008_auto_20141112_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='mobile_phone',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
