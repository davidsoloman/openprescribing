# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0046_auto_20160211_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='measureglobal',
            name='ccg_50th',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='measureglobal',
            name='practice_50th',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
