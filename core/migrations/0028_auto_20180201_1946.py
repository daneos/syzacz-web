# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20170613_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='metadata',
            field=models.CharField(default=b'{}', max_length=512),
        ),
        migrations.AddField(
            model_name='tool',
            name='metadata',
            field=models.CharField(default=b'{}', max_length=512),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 1, 19, 46, 25, 332087)),
        ),
    ]
