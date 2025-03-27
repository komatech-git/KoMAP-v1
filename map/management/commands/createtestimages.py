import io
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from map.models import Room  

def create_test_image(text, width=400, height=300, bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    """
    謖・ｮ壹＠縺溘ユ繧ｭ繧ｹ繝医ｒ荳ｭ螟ｮ縺ｫ驟咲ｽｮ縺励◆逕ｻ蜒上ｒ逕滓・縺励∪縺吶・
    """
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    # 繝輔か繝ｳ繝医・謖・ｮ夲ｼ・rial.ttf 縺御ｽｿ縺医↑縺・ｴ蜷医・繝・ヵ繧ｩ繝ｫ繝医ヵ繧ｩ繝ｳ繝医ｒ菴ｿ逕ｨ・・
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
    help = '蜷・Room 縺ｮ test_image 縺ｫ驛ｨ螻句錐縺梧嶌縺九ｌ縺溽判蜒上ｒ菫晏ｭ倥＠縺ｾ縺吶・

    def handle(self, *args, **options):
        rooms = Room.objects.all()
        for room in rooms:
            # 驛ｨ螻句錐繧堤判蜒上↓謠冗判
            image = create_test_image(room.name)
            
            # 繝舌ャ繝輔ぃ縺ｫ逕ｻ蜒上ョ繝ｼ繧ｿ繧剃ｿ晏ｭ・
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            
            # ContentFile 繧貞茜逕ｨ縺励※ Django 縺ｮ繝輔ぃ繧､繝ｫ縺ｨ縺励※謇ｱ縺・
            file_name = f"{room.name}.png"
            content = ContentFile(buffer.getvalue(), name=file_name)
            
            # Room 繧､繝ｳ繧ｹ繧ｿ繝ｳ繧ｹ縺ｮ test_image 繝輔ぅ繝ｼ繝ｫ繝峨↓菫晏ｭ假ｼ・pload_to 縺ｧ謖・ｮ壹＠縺溘ヱ繧ｹ縺ｫ譬ｼ邏阪＆繧後ｋ・・
            room.test_image.save(file_name, content, save=True)
            self.stdout.write(self.style.SUCCESS(f"Saved image for {room}"))