# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(max_length=32)),
                ('permalink', models.CharField(max_length=256)),
                ('issue_date', models.DateTimeField(default=datetime.datetime(2018, 6, 12, 12, 16, 42, 196402))),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(validators=[django.core.validators.MaxValueValidator(9999999999)], max_digits=10, decimal_places=2)),
                ('with_cashbacked', models.BooleanField()),
                ('cashbacked', models.BooleanField(default=False)),
                ('posted', models.BooleanField()),
                ('to_group', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.AlterField(
            model_name='tool',
            name='lend_permission',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='validity',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 12, 16, 42, 195402)),
        ),
        migrations.AddField(
            model_name='invoice',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
    ]
