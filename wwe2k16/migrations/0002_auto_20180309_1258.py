# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-03-09 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wwe2k16', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagteammatch',
            name='winner',
            field=models.PositiveSmallIntegerField(choices=[(b'1', b'Team 1'), (b'2', b'Team 2')], default=b'1'),
        ),
    ]
