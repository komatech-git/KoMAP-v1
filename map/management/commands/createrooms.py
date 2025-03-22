from django.core.management.base import BaseCommand
from map.models import Floor, Room

class Command(BaseCommand):
    help = '1階～9階のFloorと各部屋を作成します。特殊な部屋は辞書で指定します。'

    def handle(self, *args, **options):
        # 各階で共通して作成する部屋名
        upper3_common_rooms = ['吹き抜けエスカレーター', 'ラウンジ']  # 3階以上に必ずある部屋
        short_elevator = ['ショートエレベーター']  # 1～4階のみ設置
        long_elevator = ['ロングエレベーター']      # 1～9階に共通で設置

        # 各階ごとの特殊部屋（数値部屋とは別）を辞書で定義
        special_room_names = {
            1: ['1-2エスカレーター', '食堂', 'セブンイレブン'],
            2: ['ステージ前', '2-3エスカレーター', '1-2エスカレーター'],
            3: ['大階段の横', '3-209の前', '下りエスカレーターの前'],
            4: ['大階段の横', '下りエスカレーターの前', 'アクティブラーニングスペース', '情報グループ学習室PAO'],
            # 5～9階で特殊部屋が必要な場合は、ここに追記してください。
        }

        # 数値部屋の数を階ごとに定義（1階は例として数値部屋なし）
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
            # Floorオブジェクトを作成
            floor, floor_created = Floor.objects.get_or_create(number=floor_number)
            if floor_created:
                self.stdout.write(self.style.SUCCESS(f"Created {floor}"))

            # 数値部屋の作成（例："203", "204", ...）
            room_count = room_count_by_floor.get(floor_number, 0)
            for room_number in range(1, room_count + 1):
                room_name = f"{floor_number}{room_number:02d}"
                room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created room: {room}"))

            # 3階以上の場合、upper3_common_rooms（吹き抜けエスカレーター、ラウンジ）を作成
            if floor_number >= 3:
                for common_room in upper3_common_rooms:
                    room, room_created = Room.objects.get_or_create(floor=floor, name=common_room)
                    if room_created:
                        self.stdout.write(self.style.SUCCESS(f"Created common room: {room}"))

            # 1～4階のみ、ショートエレベーターを作成
            if floor_number in (1, 2, 3, 4):
                for se in short_elevator:
                    room, room_created = Room.objects.get_or_create(floor=floor, name=se)
                    if room_created:
                        self.stdout.write(self.style.SUCCESS(f"Created elevator room: {room}"))

            # 全階に対して、ロングエレベーターを作成
            for le in long_elevator:
                room, room_created = Room.objects.get_or_create(floor=floor, name=le)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created elevator room: {room}"))

            # 辞書に定義されている特殊部屋の作成
            if floor_number in special_room_names:
                for special_name in special_room_names[floor_number]:
                    # 空文字列はスキップ
                    if special_name.strip():
                        room, room_created = Room.objects.get_or_create(floor=floor, name=special_name)
                        if room_created:
                            self.stdout.write(self.style.SUCCESS(f"Created special room: {room}"))
