# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-02 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bikes', '0005_auto_20160801_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='user_info',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='card',
            name='user_info',
            field=models.CharField(max_length=100),
        ),
    ]
