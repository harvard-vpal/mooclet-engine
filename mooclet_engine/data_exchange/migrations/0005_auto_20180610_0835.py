# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-10 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_exchange', '0004_auto_20180610_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ontaskworkflow',
            name='url',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='qualtricssurvey',
            name='url',
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
    ]
