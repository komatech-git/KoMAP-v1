import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from map.models import Circle  # アプリ名を適宜変更してください

class Command(BaseCommand):
    help = 'BASE_DIR/data/2025_CF_dataからcircle.nameを読み込み、Circleモデルに保存します'

    def handle(self, *args, **options):
        # BASE_DIR/data/2025_CF_dataのパスを生成
        csv_file = os.path.join(settings.BASE_DIR, 'data', '2025_CF_data.csv')
        self.stdout.write(f'CSVファイルを読み込みます: {csv_file}')
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CSVのカラム"circle.name"から値を取得
                circle_name = row.get('circle.name')
                if circle_name:
                    Circle.objects.create(name=circle_name, category=None)
                    self.stdout.write(self.style.SUCCESS(f'Imported: {circle_name}'))
        
        self.stdout.write(self.style.SUCCESS('全てのcircle.nameのインポートが完了しました。'))
