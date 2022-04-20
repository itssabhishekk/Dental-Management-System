# Generated by Django 3.2.5 on 2022-04-09 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_pic/doctor_profile_pic/'),
        ),
        migrations.AlterField(
            model_name='patientuser',
            name='profile_picture',
            field=models.ImageField(default='img/defaultuser.png', upload_to='media/profile_pic/user_profile_pic/'),
        ),
    ]
