# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time_start', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('remote', models.GenericIPAddressField()),
                ('local', models.GenericIPAddressField()),
                ('session_hash', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('ldap', models.CharField(max_length=100)),
                ('cn', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to='core.User'),
        ),
    ]
