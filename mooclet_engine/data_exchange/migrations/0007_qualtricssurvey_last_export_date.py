# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-12 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_exchange', '0006_qualtricssurvey_last_survey_respondent'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualtricssurvey',
            name='last_export_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]