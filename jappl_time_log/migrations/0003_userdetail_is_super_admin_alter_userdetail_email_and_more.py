# Generated by Django 4.1.7 on 2023-03-06 13:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('jappl_time_log', '0002_alter_timelog_hour_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='is_super_admin',
            field=models.BooleanField(default=False, help_text='Is user super admin?'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='email',
            field=models.CharField(help_text="User's email", max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='first_name',
            field=models.CharField(help_text="User's first name", max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='last_name',
            field=models.CharField(help_text="User's last name", max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='password',
            field=models.CharField(help_text="User's hashed password", max_length=100),
        ),
    ]
