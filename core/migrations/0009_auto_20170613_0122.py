# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20170612_1943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='is_able',
            new_name='available',
        ),
        migrations.RemoveField(
            model_name='book',
            name='lent_permission',
        ),
        migrations.AddField(
            model_name='book',
            name='pages',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='book',
            name='review',
            field=models.CharField(default=b'Brak', max_length=4096),
        ),
        migrations.AddField(
            model_name='book',
            name='title',
            field=models.CharField(default=b'', max_length=512),
        ),
        migrations.AddField(
            model_name='lent',
            name='book',
            field=models.ForeignKey(to='core.Book', null=True),
        ),
        migrations.AlterField(
            model_name='lent',
            name='tool',
            field=models.ForeignKey(to='core.Tool', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 13, 1, 22, 45, 582000)),
        ),
    ]
