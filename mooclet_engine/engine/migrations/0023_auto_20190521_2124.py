# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-21 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0022_auto_20190102_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]