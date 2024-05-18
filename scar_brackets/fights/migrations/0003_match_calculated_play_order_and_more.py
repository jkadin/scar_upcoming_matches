# Generated by Django 5.0.4 on 2024-05-18 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0002_match_player1_id_match_player2_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="calculated_play_order",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="match",
            name="estimated_start_time",
            field=models.DateTimeField(null=True),
        ),
    ]
