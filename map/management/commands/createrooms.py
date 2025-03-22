from django.core.management.base import BaseCommand
from map.models import Floor, Room

class Command(BaseCommand):
    help = '1階～9階のFloorと、各部屋を作成します。また、特殊な部屋も製作します。ex:ステージ前 など。'

    def handle(self, *args, **options):
        for floor_number in range(1, 10):
            floor, created = Floor.objects.get_or_create(number=floor_number)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {floor}"))

            if floor_number == 2:
                for room_number in range(1,13):
                    room_name = f"{floor_number}{room_number:02d}"
                    room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
                room_name = "ステージ前"
                room, room_created = Room.objects.get_or_create(floor = floor, name= room_name)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {room}"))

            if floor_number == 3:
                for room_number in range(1,13):
                    room_name = f"{floor_number}{room_number:02d}"
                    room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
                
                room_names = ["大階段の横", "3-209の前","下りエスカレーターの前","ラウンジ"]  
                for name in room_names:
                    room, room_created = Room.objects.get_or_create(floor=floor, name=name)

                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {room}"))
                
            elif floor_number == 4:
                for room_number in range(1,11):
                    room_name = f"{floor_number}{room_number:02d}"
                    room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
            
                room_names = ["大階段の横","下りエスカレーターの前", "アクティブラーニングスペース" ,"情報グループ学習室PAO","ラウンジ"]  
                for name in room_names:
                    room, room_created = Room.objects.get_or_create(floor=floor, name=name)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {room}"))

            elif floor_number == 5:
                for room_number in range(1,6):
                    room_name = f"{floor_number}{room_number:02d}"
                    room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)

                room_names = ["ラウンジ"]  
                for name in room_names:
                    room, room_created = Room.objects.get_or_create(floor=floor, name=name)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {room}"))
            

            elif floor_number in (6,7):
                for room_number in range(1,7):
                    room_name = f"{floor_number}{room_number:02d}"
                    room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
                    
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {room}"))
                
                lounge_room, lounge_created = Room.objects.get_or_create(floor=floor, name="ラウンジ")
                if lounge_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {lounge_room}"))

            #本当はfloor_number== 2 or 3と同じ処理だが、可読性のために8 or 9と書く。
            elif floor_number in (8,9):
                for room_number in range(1,13):
                    room_name = f"{floor_number}{room_number:02d}"
                    room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {room}"))

                lounge_room, lounge_created = Room.objects.get_or_create(floor=floor, name="ラウンジ")
                if lounge_created:
                    self.stdout.write(self.style.SUCCESS(f"Created {lounge_room}"))


