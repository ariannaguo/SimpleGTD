# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simgtd', '0005_auto_20141103_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='status',
            field=models.ForeignKey(default=1, to='simgtd.Status'),
            preserve_default=True,
        ),
    ]
