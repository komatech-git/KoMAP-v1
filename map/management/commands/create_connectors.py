from django.core.management.base import BaseCommand
from map.models import Connector, Floor

class Command(BaseCommand):
    help = "Create Connector entries: short_elevator for floors 1-4 and long_elevator for floors 1-9."

    def handle(self, *args, **options):
        floors = Floor.objects.all()
        for floor in floors:
            # long_elevator繧・・・髫弱↓菴懈・
            if 1 <= floor.number <= 9:
                long_elevator, created = Connector.objects.get_or_create(
                    floor=floor,
                    name="long_elevator"
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created long_elevator for Floor {floor.number}"
                    ))
                else:
                    self.stdout.write(
                        f"long_elevator for Floor {floor.number} already exists."
                    )

            # short_elevator繧・・・髫弱↓菴懈・
            if 1 <= floor.number <= 4:
                short_elevator, created = Connector.objects.get_or_create(
                    floor=floor,
                    name="short_elevator"
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created short_elevator for Floor {floor.number}"
                    ))
                else:
                    self.stdout.write(
                        f"short_elevator for Floor {floor.number} already exists."
                    )
        self.stdout.write(self.style.SUCCESS("Connector entries have been created successfully."))