# Generated by Django 5.0.4 on 2024-04-24 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0018_match_suggested_play_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="suggested_play_order",
            field=models.IntegerField(),
        ),
    ]