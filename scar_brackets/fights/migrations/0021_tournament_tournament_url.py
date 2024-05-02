# Generated by Django 5.0.4 on 2024-05-02 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0020_remove_url_id_alter_url_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournament",
            name="tournament_url",
            field=models.ForeignKey(
                default="self",
                on_delete=django.db.models.deletion.CASCADE,
                to="fights.url",
            ),
            preserve_default=False,
        ),
    ]
