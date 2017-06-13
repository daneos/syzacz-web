# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20170613_0239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='to_group',
        ),
        migrations.AddField(
            model_name='invoice',
            name='group',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 13, 10, 26, 39, 295000)),
        ),
    ]
