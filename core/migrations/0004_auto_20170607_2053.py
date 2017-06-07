# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('lent_date', models.DateTimeField(auto_now_add=True)),
                ('planned_return_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateTimeField()),
                ('comment', models.CharField(max_length=256)),
                ('member_id', models.ForeignKey(to='core.User')),
            ],
        ),
        migrations.CreateModel(
            name='Lent_form',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('lent_date', models.DateTimeField(auto_now_add=True)),
                ('planned_return_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=256)),
                ('permission', models.BooleanField(default=False)),
                ('member_id', models.ForeignKey(to='core.User')),
            ],
        ),
        migrations.CreateModel(
            name='Members_special_function',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_id', models.ForeignKey(to='core.User')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('user_priority', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('description', models.CharField(max_length=512)),
                ('member_id', models.ForeignKey(to='core.User')),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('room_name', models.CharField(max_length=32)),
                ('rack_id', models.CharField(max_length=32)),
                ('additinal_information', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('priority_name', models.CharField(max_length=32)),
                ('priority_level', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=512)),
                ('remained', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('remained_alarm', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
            ],
        ),
        migrations.CreateModel(
            name='Resource_using',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('use_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('comment', models.CharField(max_length=256)),
                ('member_id', models.ForeignKey(to='core.User')),
                ('resource_id', models.ForeignKey(to='core.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='Special_function',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('function_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=512)),
                ('is_able', models.BooleanField(default=True)),
                ('lent_permission', models.BooleanField(default=True)),
                ('member_id', models.ForeignKey(to='core.User')),
                ('placement_id', models.ForeignKey(to='core.Placement')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='priority_id',
            field=models.ForeignKey(to='core.Priority'),
        ),
        migrations.AddField(
            model_name='members_special_function',
            name='priority_id',
            field=models.ForeignKey(to='core.Special_function'),
        ),
        migrations.AddField(
            model_name='lent_form',
            name='tool_id',
            field=models.ForeignKey(to='core.Tool'),
        ),
        migrations.AddField(
            model_name='lent',
            name='tool_id',
            field=models.ForeignKey(to='core.Tool'),
        ),
    ]
