# Generated by Django 5.0.4 on 2024-06-26 16:44

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0011_alter_option_option_name_alter_option_option_value"),
        ("preferences", "0003_alter_preferences_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="MyPreferences",
            fields=[
                (
                    "preferences_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="preferences.preferences",
                    ),
                ),
                (
                    "interleave_method",
                    models.CharField(
                        blank=True, default="Fixed", max_length=100, null=True
                    ),
                ),
            ],
            bases=("preferences.preferences",),
            managers=[
                ("singleton", django.db.models.manager.Manager()),
            ],
        ),
    ]
