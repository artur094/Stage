# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_auto_20160218_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentedPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='photos',
            name='id_owner',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='hello.User'),
        ),
        migrations.AddField(
            model_name='commentedphoto',
            name='id_photos',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='hello.Photos'),
        ),
        migrations.AddField(
            model_name='commentedphoto',
            name='id_reporter',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='hello.User'),
        ),
    ]