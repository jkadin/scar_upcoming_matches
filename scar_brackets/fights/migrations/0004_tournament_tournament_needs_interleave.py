# Generated by Django 5.0.4 on 2024-05-21 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0003_match_calculated_play_order_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournament",
            name="tournament_needs_interleave",
            field=models.BooleanField(default=True),
        ),
    ]