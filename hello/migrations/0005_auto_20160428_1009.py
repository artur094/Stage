# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 10:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_auto_20160428_0938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='magazine_type',
            old_name='id_magazine',
            new_name='magazine',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='magazine',
        ),
        migrations.AddField(
            model_name='photo',
            name='magazine_type',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='hello.Magazine_type'),
        ),
    ]
