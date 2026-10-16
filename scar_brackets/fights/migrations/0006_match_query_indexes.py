from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fights", "0005_notification"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="match",
            index=models.Index(
                fields=["player1_id", "match_state", "-updated_at"],
                name="match_p1_state_updated_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="match",
            index=models.Index(
                fields=["player2_id", "match_state", "-updated_at"],
                name="match_p2_state_updated_idx",
            ),
        ),
    ]