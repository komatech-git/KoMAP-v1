import io
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from map.models import Room  

def create_test_image(text, width=400, height=300, bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    """
    部屋の名前を中央に配置した画像を生成します
    """
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    # フォント�E持E��！Erial.ttf が使えなぁE��合�EチE��ォルトフォントを使用�E�E
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, fill=text_color, font=font)
    return image

class Command(BaseCommand):
    help = 'Room の test_image に部屋名が書かれた画像を保存します'

    def handle(self, *args, **options):
        rooms = Room.objects.all()
        for room in rooms:
            # 部屋名を画像に描画
            image = create_test_image(room.name)
            
            # バッファに画像データを保孁E
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            
            # ContentFile を利用して Django のファイルとして扱ぁE
            file_name = f"{room.name}.png"
            content = ContentFile(buffer.getvalue(), name=file_name)
            
            # Room インスタンスの test_image フィールドに保存！Epload_to で持E��したパスに格納される�E�E
            room.test_image.save(file_name, content, save=True)
            self.stdout.write(self.style.SUCCESS(f"Saved image for {room}"))