# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20170607_2053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tool',
            old_name='is_able',
            new_name='available',
        ),
    ]
