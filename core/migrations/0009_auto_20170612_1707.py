# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20170612_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 17, 7, 33, 801544)),
        ),
    ]
