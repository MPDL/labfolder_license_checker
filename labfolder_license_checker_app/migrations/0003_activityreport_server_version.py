# Generated by Django 2.2.10 on 2020-03-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labfolder_license_checker_app', '0002_activityreport_active_users_last_6_months'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityreport',
            name='server_version',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
    ]