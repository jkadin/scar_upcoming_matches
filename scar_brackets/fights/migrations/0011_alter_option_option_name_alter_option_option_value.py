# Generated by Django 5.0.4 on 2024-06-25 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0010_remove_option_id_remove_option_interleave_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="option_name",
            field=models.CharField(
                default="Interleave type",
                max_length=100,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="option",
            name="option_value",
            field=models.CharField(default="Recalc", max_length=100),
        ),
    ]
