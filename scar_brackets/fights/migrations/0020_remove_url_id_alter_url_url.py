# Generated by Django 5.0.4 on 2024-05-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0019_alter_match_suggested_play_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="url",
            name="id",
        ),
        migrations.AlterField(
            model_name="url",
            name="url",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
