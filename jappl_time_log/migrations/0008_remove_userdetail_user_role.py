# Generated by Django 4.1.7 on 2023-03-14 10:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('jappl_time_log', '0007_alter_userdetail_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetail',
            name='user_role',
        ),
    ]
