# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-15 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20181014_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkDownModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('content', mdeditor.fields.MDTextField()),
            ],
        ),
    ]
