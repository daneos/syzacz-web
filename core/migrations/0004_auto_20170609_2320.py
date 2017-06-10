# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170608_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tool',
            old_name='lent_permission',
            new_name='lend_permission',
        ),
        migrations.RenameField(
            model_name='tool',
            old_name='member_id',
            new_name='member',
        ),
        migrations.RenameField(
            model_name='tool',
            old_name='placement_id',
            new_name='placement',
        ),
        migrations.AlterField(
            model_name='lent',
            name='planned_return_date',
            field=models.DateTimeField(),
        ),
    ]
