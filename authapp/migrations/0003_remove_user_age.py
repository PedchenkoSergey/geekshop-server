# Generated by Django 3.2 on 2021-05-06 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_user_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
    ]