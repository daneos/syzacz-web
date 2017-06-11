# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170608_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 9, 22, 53, 34, 827000)),
        ),
    ]
