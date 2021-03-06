# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 21:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bikes', '0011_auto_20160801_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Bikes.Order'),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Bikes.Order'),
        ),
        migrations.AlterField(
            model_name='preorders',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bikes.Billing'),
        ),
        migrations.AlterField(
            model_name='preorders',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bikes.Card'),
        ),
    ]
