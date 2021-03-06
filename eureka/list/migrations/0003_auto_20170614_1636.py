# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0002_auto_20170612_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='priority',
            field=models.PositiveIntegerField(choices=[('1', 'high'), ('2', 'medium'), ('3', 'normal'), ('4', 'low')]),
        ),
        migrations.AlterField(
            model_name='list',
            name='priority',
            field=models.PositiveIntegerField(choices=[('1', 'high'), ('2', 'medium'), ('3', 'normal'), ('4', 'low')]),
        ),
    ]
