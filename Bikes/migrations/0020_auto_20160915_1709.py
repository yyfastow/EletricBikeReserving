# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 21:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bikes', '0019_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='bike',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]