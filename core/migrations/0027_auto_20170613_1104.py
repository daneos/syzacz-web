# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='file',
            field=models.FileField(null=True, upload_to=b'storage/syzacz/faktury'),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 13, 11, 4, 49, 329449)),
        ),
    ]
