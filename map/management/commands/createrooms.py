from django.core.management.base import BaseCommand
from map.models import Floor, Room

class Command(BaseCommand):
    help = '1髫趣ｽ・髫弱・Floor縺ｨ蜷・Κ螻九ｒ菴懈・縺励∪縺吶ら音谿翫↑驛ｨ螻九・霎樊嶌縺ｧ謖・ｮ壹＠縺ｾ縺吶・

    def handle(self, *args, **options):
        # 蜷・嚴縺ｧ蜈ｱ騾壹＠縺ｦ菴懈・縺吶ｋ驛ｨ螻句錐
        upper3_common_rooms = ['繝ｩ繧ｦ繝ｳ繧ｸ']  # 3髫惹ｻ･荳翫↓蠢・★縺ゅｋ驛ｨ螻・

        # 蜷・嚴縺斐→縺ｮ迚ｹ谿企Κ螻具ｼ域焚蛟､驛ｨ螻九→縺ｯ蛻･・峨ｒ霎樊嶌縺ｧ螳夂ｾｩ
        special_room_names = {
            1: ['鬟溷・, '繧ｻ繝悶Φ繧､繝ｬ繝悶Φ'],
            2: ['繧ｹ繝・・繧ｸ蜑・, ],
            3: ['螟ｧ髫取ｮｵ縺ｮ讓ｪ', '3-209縺ｮ蜑・,'繧｢繧ｯ繝・ぅ繝悶Λ繝ｼ繝九Φ繧ｰ繧ｹ繝壹・繧ｹ', '荳九ｊ繧ｨ繧ｹ繧ｫ繝ｬ繝ｼ繧ｿ繝ｼ莉倩ｿ・],
            4: ['螟ｧ髫取ｮｵ縺ｮ讓ｪ', '荳九ｊ繧ｨ繧ｹ繧ｫ繝ｬ繝ｼ繧ｿ繝ｼ莉倩ｿ・, '繧｢繧ｯ繝・ぅ繝悶Λ繝ｼ繝九Φ繧ｰ繧ｹ繝壹・繧ｹ', '諠・ｱ繧ｰ繝ｫ繝ｼ繝怜ｭｦ鄙貞ｮ､PAO','諠・ｱ繧ｰ繝ｫ繝ｼ繝怜ｭｦ鄙貞ｮ､縺ｮ蜑・],
            # 5・・髫弱〒迚ｹ谿企Κ螻九′蠢・ｦ√↑蝣ｴ蜷医・縲√％縺薙↓霑ｽ險倥＠縺ｦ縺上□縺輔＞縲・
        }

        # 謨ｰ蛟､驛ｨ螻九・謨ｰ繧帝嚴縺斐→縺ｫ螳夂ｾｩ・・髫弱・萓九→縺励※謨ｰ蛟､驛ｨ螻九↑縺暦ｼ・
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
            # Floor繧ｪ繝悶ず繧ｧ繧ｯ繝医ｒ菴懈・
            floor, floor_created = Floor.objects.get_or_create(number=floor_number)
            if floor_created:
                self.stdout.write(self.style.SUCCESS(f"Created {floor}"))

            # 謨ｰ蛟､驛ｨ螻九・菴懈・・井ｾ具ｼ・203", "204", ...・・
            room_count = room_count_by_floor.get(floor_number, 0)
            for room_number in range(1, room_count + 1):
                room_name = f"3-{floor_number}{room_number:02d}"
                room, room_created = Room.objects.get_or_create(floor=floor, name=room_name)
                if room_created:
                    self.stdout.write(self.style.SUCCESS(f"Created room: {room}"))

            # 3髫惹ｻ･荳翫・蝣ｴ蜷医「pper3_common_rooms・亥聖縺肴栢縺代お繧ｹ繧ｫ繝ｬ繝ｼ繧ｿ繝ｼ縲√Λ繧ｦ繝ｳ繧ｸ・峨ｒ菴懈・
            if floor_number >= 3:
                for common_room in upper3_common_rooms:
                    room, room_created = Room.objects.get_or_create(floor=floor, name=common_room)
                    if room_created:
                        self.stdout.write(self.style.SUCCESS(f"Created common room: {room}"))

            # 霎樊嶌縺ｫ螳夂ｾｩ縺輔ｌ縺ｦ縺・ｋ迚ｹ谿企Κ螻九・菴懈・
            if floor_number in special_room_names:
                for special_name in special_room_names[floor_number]:
                    # 遨ｺ譁・ｭ怜・縺ｯ繧ｹ繧ｭ繝・・
                    if special_name.strip():
                        room, room_created = Room.objects.get_or_create(floor=floor, name=special_name)
                        if room_created:
                            self.stdout.write(self.style.SUCCESS(f"Created special room: {room}"))