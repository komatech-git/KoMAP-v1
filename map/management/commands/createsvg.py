import os
from django.core.management.base import BaseCommand
from django.conf import settings
from map.models import Floor

class Command(BaseCommand):
    help = 'Load SVG files from BASE_DIR/data and store them in Floor.svg_text'

    def handle(self, *args, **options):
        base_path = os.path.join(settings.BASE_DIR, 'data')
        for i in range(1, 10):
            filename = f'floor{i}_image.svg'
            filepath = os.path.join(base_path, filename)

            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as svg_file:
                    svg_content = svg_file.read()

                floor_obj, created = Floor.objects.get_or_create(number=i)
                floor_obj.svg_text = svg_content
                floor_obj.save()

                self.stdout.write(self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} Floor {i} with {filename}"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"SVG file not found: {filename}"
                ))