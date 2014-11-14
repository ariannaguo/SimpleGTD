# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simgtd', '0009_auto_20141112_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actioncomment',
            name='action',
            field=models.ForeignKey(related_name=b'comments', to='simgtd.Action'),
        ),
    ]
