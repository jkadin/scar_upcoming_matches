# Generated by Django 5.0.4 on 2024-04-22 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0006_rename_tourament_tournament_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="match",
            name="id",
        ),
        migrations.AlterField(
            model_name="match",
            name="match_id",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]