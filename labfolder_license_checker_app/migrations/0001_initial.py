# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportmonth', models.DateField(default=None)),
                ('registered_users', models.BigIntegerField(default=None)),
            ],
            options={
                'ordering': ['-reportmonth', 'instance__name'],
            },
        ),
        migrations.CreateModel(
            name='ActivityReportEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('activity_count', models.BigIntegerField()),
                ('activity_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labfolder_license_checker_app.ActivityReport')),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=512, unique=True)),
                ('moderator_name', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('moderator_email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=512, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='instance',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labfolder_license_checker_app.Institute'),
        ),
        migrations.AddField(
            model_name='activityreport',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labfolder_license_checker_app.Instance'),
        ),
        migrations.AlterUniqueTogether(
            name='activityreport',
            unique_together=set([('instance', 'reportmonth')]),
        ),
    ]