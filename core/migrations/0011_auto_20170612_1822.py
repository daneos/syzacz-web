# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170612_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('invoice_number', models.CharField(max_length=32)),
                ('permalink', models.CharField(max_length=256)),
                ('issue_date', models.DateTimeField(default=datetime.datetime(2018, 6, 12, 18, 22, 24, 301000))),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2, validators=[django.core.validators.MaxValueValidator(9999999999L)])),
                ('with_cashbacked', models.BooleanField()),
                ('cashbacked', models.BooleanField(default=False)),
                ('posted', models.BooleanField()),
                ('to_group', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 18, 22, 24, 300000)),
        ),
        migrations.AddField(
            model_name='invoice',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
    ]
