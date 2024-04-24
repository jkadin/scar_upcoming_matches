from django.core.management.base import BaseCommand, CommandError
from fights.views import update_database


class Command(BaseCommand):
    help = "Updates the data from the API"

    def handle(self, *args, **options):
        update_database()

        self.stdout.write(self.style.SUCCESS("Successfully updated data"))


def main():
    update_database()


if __name__ == "__name__":
    main()
