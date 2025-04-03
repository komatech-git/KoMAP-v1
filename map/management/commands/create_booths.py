import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from map.models import Circle, Booth, Room  # 必要なモデルをインポート

class Command(BaseCommand):
    help = 'CSVファイルからcircleとboothを作成します。circleは既にimport_circle_names.pyで作成済み、roomsは他のコマンドで作成済みです。'

    def handle(self, *args, **options):
        # CSVファイルのパスを指定
        csv_file = os.path.join(settings.BASE_DIR, 'data', '2025_CF_data.csv')
        self.stdout.write(f'CSVファイルを読み込みます: {csv_file}')

        # CSVの全行をリストに保存（circle作成後、booth作成でも利用）
        rows = []
        with open(csv_file, 'r', encoding='utf-8-sig' ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
                # circle.nameカラムからCircleを作成（既に存在する場合は取得）
                circle_name = row.get('circle.name')
                if circle_name:
                    circle, created = Circle.objects.get_or_create(name=circle_name, defaults={'category': None})
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Imported Circle: {circle_name}'))
                    else:
                        self.stdout.write(f'Circle already exists: {circle_name}')

        self.stdout.write(self.style.SUCCESS('全てのcircle.nameのインポートが完了しました。'))

        # CSVファイルの各行について、room.nameカラムを利用してBoothを作成
        for row in rows:
            floor_number = row.get('floor.number')
            circle_name = row.get('circle.name')
            room_name = row.get('room.name')

            if not circle_name or not room_name or not floor_number:
                self.stdout.write('circle.nameまたはroom.name, floor_numberの情報が不足している行をスキップします。')
                continue

            # 既存のCircleとRoomを取得
            circle = Circle.objects.filter(name=circle_name).first()
            room = Room.objects.filter(name=room_name, floor__number=floor_number).first()

            if circle and room:
                booth, created = Booth.objects.get_or_create(circle=circle, room=room)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created Booth: {circle_name} in {room_name}'))
                else:
                    self.stdout.write(f'Booth already exists: {circle_name} in {room_name}')
            else:
                if not circle:
                    self.stdout.write(f'Circleが見つかりませんでした: {circle_name}')
                if not room:
                    self.stdout.write(f'Roomが見つかりませんでした: {room_name},{floor_number}')

        self.stdout.write(self.style.SUCCESS('全てのbooth作成が完了しました。'))
