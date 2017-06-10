# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20170609_2320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lent',
            old_name='member_id',
            new_name='member',
        ),
        migrations.RenameField(
            model_name='lent',
            old_name='tool_id',
            new_name='tool',
        ),
    ]
