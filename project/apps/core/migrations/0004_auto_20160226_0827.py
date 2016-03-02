# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-26 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160223_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=250)),
                ('priority', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Colors',
                'verbose_name': 'Color',
            },
        ),
        migrations.CreateModel(
            name='Palette',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('likes_count', models.IntegerField(default=1)),
                ('is_featured', models.BooleanField(default=False)),
                ('date_featured', models.DateTimeField(blank=True, null=True)),
                ('colors', models.ManyToManyField(blank=True, related_name='palette_colors', to='core.Color')),
                ('likes', models.ManyToManyField(blank=True, related_name='palette_likes', to='core.Profile')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Profile')),
            ],
            options={
                'verbose_name_plural': 'Palettes',
                'verbose_name': 'Palette',
            },
        ),
        migrations.AlterField(
            model_name='gradientpalette',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='gradient_likes', to='core.Profile'),
        ),
    ]
