# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170612_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='member_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 12, 19, 42, 890738)),
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
    ]
