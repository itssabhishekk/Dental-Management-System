# Generated by Django 3.2.5 on 2022-03-29 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20220329_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='service',
        ),
        migrations.AlterField(
            model_name='patientuser',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 17, 57, 1, 283360)),
        ),
    ]