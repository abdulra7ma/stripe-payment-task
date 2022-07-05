# Generated by Django 4.1b1 on 2022-07-04 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LoginDevice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("device", models.CharField(blank=True, max_length=150, null=True)),
                ("os", models.CharField(blank=True, max_length=150, null=True)),
                ("browser", models.CharField(blank=True, max_length=150, null=True)),
                ("ip_address", models.CharField(blank=True, max_length=45, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("last_login", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_registered", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-id",),
            },
        ),
    ]
