# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-01-27 13:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0015_auto_20170126_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ppqsaving',
            name='price_per_dose',
            field=models.FloatField(),
        )
    ]