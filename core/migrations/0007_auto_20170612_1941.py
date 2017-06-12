# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceUsage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField()),
                ('comment', models.CharField(max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='lent_form',
            name='member_id',
        ),
        migrations.RemoveField(
            model_name='lent_form',
            name='tool_id',
        ),
        migrations.RemoveField(
            model_name='resource_using',
            name='member_id',
        ),
        migrations.RemoveField(
            model_name='resource_using',
            name='resource_id',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='remained',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='remained_alarm',
        ),
        migrations.AddField(
            model_name='resource',
            name='alarm',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tool',
            name='lend_permission',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 19, 40, 58, 864820)),
        ),
        migrations.DeleteModel(
            name='Lent_form',
        ),
        migrations.DeleteModel(
            name='Resource_using',
        ),
        migrations.AddField(
            model_name='resourceusage',
            name='member',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='resourceusage',
            name='resource',
            field=models.ForeignKey(to='core.Resource'),
        ),
    ]
