from django.core.management.base import BaseCommand
from map.models import Booth  # アプリ名に合わせて適宜修正してください

class Command(BaseCommand):
    help = 'Deletes all Booth objects from the database'

    def handle(self, *args, **kwargs):
        num_deleted, _ = Booth.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {num_deleted} Booth object{'s' if num_deleted != 1 else ''}."
        ))