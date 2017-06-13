# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20170613_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='file',
            field=models.FileField(null=True, upload_to=set([b'/syzacz/0/0/4/testing/syzacz/faktury'])),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 13, 2, 1, 47, 676000)),
        ),
    ]
