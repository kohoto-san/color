# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-28 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160227_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagepalette',
            name='original_url',
            field=models.URLField(null=True),
        ),
    ]
