# Generated by Django 5.0.4 on 2024-04-21 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0003_matches"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Matches",
            new_name="Match",
        ),
    ]
