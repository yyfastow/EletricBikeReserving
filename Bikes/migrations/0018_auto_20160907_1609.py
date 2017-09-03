# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bikes', '0017_auto_20160817_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikes',
            name='PAS',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='battery',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='brake_lever',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='chain',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='chain_wheel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='charger',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='charging_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='container_load',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='controller',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='derailleur',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='display',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='frame',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='front_brake',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='front_fork',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='gross_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='max_load',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='max_speed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='motor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='mudguard',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='net_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='packaging_size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='pedal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='range',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='rear_break',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='rim',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='saddle',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='speed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='stem',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='tyres',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='biketypes',
            name='picture',
            field=models.ImageField(upload_to='images'),
        ),
    ]