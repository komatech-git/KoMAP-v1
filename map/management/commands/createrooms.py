from django.core.management.base import BaseCommand
from map.models import Floor, Room

class Command(BaseCommand):
    help = '1階から9階までの部屋を制作します'

    def handle(self, *args, **options):
        # 吁E��で共通して作�Eする部屋名
        upper3_common_rooms = ['ラウンジ']  # 3階以上に忁E��ある部屁E

        # 吁E��ごとの特殊部屋（数値部屋とは別�E�を辞書で定義
        special_room_names = {
            1: ['食堂', 'セブンイレブン'],
            2: ['ステージ横', '3-208/209' ],
            3: ['大階段の横', '3-209の前','アクティブラーニングスペース', '下りエスカレーター付迁'],
            4: ['大階段の横', '下りエスカレーター付近', 'アクティブラーニングスペース', '情報グループ学習室PAO','情報グループ学習室の前'],
            # 5�E�E階で特殊部屋が忁E��な場合�E、ここに追記してください、E
        }

        # 数値部屋�E数を階ごとに定義�E�E階�E例として数値部屋なし！E
        room_count_by_floor = {
            2: 12,
            3: 12,
            4: 10,
            5: 5,
            6: 6,
            7: 6,
            8: 12,
            9: 12,
        }

        for floor_number in range(1, 10):
            # Floorオブジェクトを作�E
            floor, floor_created = Floor.objects.get_or_create(number=floor_number)
            if floor_created:
                self.stdout.write(self.style.SUCCESS(f"Created {floor}"))

            # 数値部屋�E作�E�E�例！E203", "204", ...�E�E
            room_count = room_count_by_floor.get(floor_number, 0)
            for room_number in range(1, room_count + 1):
                room_name = f"3-{floor_number}{room_number:02d}"
                room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created room: {room}"))

            # 3階以上�E場合、upper3_common_rooms�E�吹き抜けエスカレーター、ラウンジ�E�を作�E
            if floor_number >= 3:
                for common_room in upper3_common_rooms:
                    room, room_created = Room.objects.get_or_create(floor=floor, name=common_room)
                    if room_created:
                        self.stdout.write(self.style.SUCCESS(f"Created common room: {room}"))

            # 辞書に定義されてぁE��特殊部屋�E作�E
            if floor_number in special_room_names:
                for special_name in special_room_names[floor_number]:
                    # 空斁E���EはスキチE�E
                    if special_name.strip():
                        room, room_created = Room.objects.get_or_create(floor=floor, name=special_name)
                        if room_created:
                            self.stdout.write(self.style.SUCCESS(f"Created special room: {room}"))