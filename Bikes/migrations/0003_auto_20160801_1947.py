# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-01 23:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bikes', '0002_auto_20160801_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing',
            name='user_info',
        ),
        migrations.RemoveField(
            model_name='card',
            name='user_info',
        ),
        migrations.RemoveField(
            model_name='preorders',
            name='address',
        ),
        migrations.RemoveField(
            model_name='preorders',
            name='payment',
        ),
    ]
