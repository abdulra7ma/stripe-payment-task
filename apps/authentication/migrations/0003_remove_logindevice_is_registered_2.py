# Generated by Django 4.1b1 on 2022-07-04 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_logindevice_is_registered_2"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="logindevice",
            name="is_registered_2",
        ),
    ]
