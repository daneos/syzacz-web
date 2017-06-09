# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=512)),
                ('is_able', models.BooleanField(default=True)),
                ('lent_permission', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('lent_date', models.DateTimeField(auto_now_add=True)),
                ('planned_return_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateTimeField()),
                ('comment', models.CharField(max_length=256)),
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
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Members_special_function',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('user_priority', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('description', models.CharField(max_length=512)),
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
                ('available', models.BooleanField(default=True)),
                ('lent_permission', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AddField(
            model_name='tool',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='tool',
            name='placement_id',
            field=models.ForeignKey(to='core.Placement'),
        ),
        migrations.AddField(
            model_name='resource_using',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='resource_using',
            name='resource_id',
            field=models.ForeignKey(to='core.Resource'),
        ),
        migrations.AddField(
            model_name='notification',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='notification',
            name='priority_id',
            field=models.ForeignKey(to='core.Priority'),
        ),
        migrations.AddField(
            model_name='members_special_function',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='members_special_function',
            name='priority_id',
            field=models.ForeignKey(to='core.Special_function'),
        ),
        migrations.AddField(
            model_name='lent_form',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='lent_form',
            name='tool_id',
            field=models.ForeignKey(to='core.Tool'),
        ),
        migrations.AddField(
            model_name='lent',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='lent',
            name='tool_id',
            field=models.ForeignKey(to='core.Tool'),
        ),
        migrations.AddField(
            model_name='book',
            name='member_id',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='book',
            name='placement_id',
            field=models.ForeignKey(to='core.Placement'),
        ),
    ]
