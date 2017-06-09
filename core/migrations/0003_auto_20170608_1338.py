# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170608_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lent',
            name='return_date',
            field=models.DateTimeField(null=True),
        ),
    ]
