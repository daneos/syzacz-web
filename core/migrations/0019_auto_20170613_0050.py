# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170612_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='file',
            field=models.FileField(null=True, upload_to=b'syzacz/faktury'),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 13, 0, 50, 51, 264000)),
        ),
    ]
