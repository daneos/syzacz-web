# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170612_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='issue_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 18, 31, 20, 214000)),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 18, 31, 20, 214000)),
        ),
    ]
