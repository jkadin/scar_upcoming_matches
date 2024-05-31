# Generated by Django 5.0.4 on 2024-05-31 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0009_rename_options_option"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="option",
            name="id",
        ),
        migrations.RemoveField(
            model_name="option",
            name="interleave_type",
        ),
        migrations.AddField(
            model_name="option",
            name="option_name",
            field=models.CharField(
                default="Interleave type",
                max_length=100,
                primary_key=True,
                serialize=False,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="option",
            name="option_value",
            field=models.CharField(default="Interleave type", max_length=100),
            preserve_default=False,
        ),
    ]