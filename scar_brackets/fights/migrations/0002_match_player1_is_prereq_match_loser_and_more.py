# Generated by Django 5.0.4 on 2024-06-30 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="player1_is_prereq_match_loser",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="match",
            name="player2_is_prereq_match_loser",
            field=models.BooleanField(default=False),
        ),
    ]
