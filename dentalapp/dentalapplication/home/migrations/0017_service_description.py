# Generated by Django 3.2.5 on 2022-04-16 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20220410_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.TextField(default='this is a great service'),
            preserve_default=False,
        ),
    ]
