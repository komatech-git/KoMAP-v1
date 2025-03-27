from django.shortcuts import render, redirect
from django.views import View
from . models import QRViewCount, Booth, Floor
from django.urls import reverse
from django.http import JsonResponse
from .forms import NavigationForm
import datetime
from urllib.parse import urlencode
# Create your views here.

class IndexView(View):
    def get(self, request):
        form = NavigationForm()
        # booth繧偵Λ繝ｳ繝繝縺ｫ3莉ｶ陦ｨ遉ｺ縺吶ｋ
        booths = Booth.objects.order_by('?')[:3]
        
        booth_info = []
        for booth in booths:
            circle_name = booth.circle.name if booth.circle else "譛ｪ險ｭ螳・
            room_name = booth.room.name if booth.room else "譛ｪ險ｭ螳・
            # 邨先棡繝壹・繧ｸ縺ｮURL縺ｫbooth_id繧偵け繧ｨ繝ｪ繝代Λ繝｡繝ｼ繧ｿ縺ｨ縺励※莉倅ｸ・
            url = reverse('map:result') + f'?booth_id={booth.id}'
            booth_info.append({
                "circle_name": circle_name,
                "room_name": room_name,
                "url": url,
            })

        context = {
            'form': form,
            'booth_info': booth_info,
        }
        return render(request, 'map/index.html', context)
    
    def post(self, request):
        form = NavigationForm(request.POST)
        if form.is_valid():
            current_charfloor = form.cleaned_data['floor']
            current_floor = int(current_charfloor)
            booth_query = form.cleaned_data['booth']
            booth_instance = Booth.objects.filter(circle__name__icontains=booth_query).first()
                
            if not booth_instance:
                context = {
                    'form': form,
                    'destination': "謖・ｮ壹＆繧後◆繝悶・繧ｹ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ縺ｧ縺励◆",
                }
                return render(request, 'map/index.html', context)
            else:
                query_params = {
                    'booth_id':booth_instance.id,
                    'current_floor': current_charfloor,
                    'booth':booth_query,
                }
                url = reverse('map:result') + '?' + urlencode(query_params)
                return redirect(url)
        return render(request, 'map/index.html', {'form': form})


class ResultView(View):
    def get(self, request, **kwargs):


        booth_id = request.GET.get('booth_id')
        current_floor = request.GET.get('current_floor')
        
        # current_floor縺梧枚蟄怜・縺ｧ貂｡縺輔ｌ繧九・縺ｧ縲∵焚蛟､縺ｫ螟画鋤・亥､画鋤縺ｧ縺阪↑縺代ｌ縺ｰNone・・
        if current_floor is not None:
            try:
                current_floor = int(current_floor)
                current_floor_instance = Floor.objects.get(number=current_floor)
            except ValueError:
                current_floor = None
        
        if booth_id is None:
            destination = "蠢・ｦ√↑諠・ｱ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ縺ｧ縺励◆縲ょ・蠎ｦ蜈･蜉帙＠縺ｦ縺上□縺輔＞"
            return render(request, 'map/index.html', {'form': form, 'destination': destination})
        
        try:
            booth = Booth.objects.get(pk=booth_id)
        except Booth.DoesNotExist:
            destination = "謖・ｮ壹＆繧後◆繝悶・繧ｹ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ縺ｧ縺励◆"
            return render(request, 'map/index.html', {'form': form, 'destination': destination})
        
        instructions = {
            'intro':[],
            'floor_move':[],
            'room_guide':[],
        } 
        destination_floor = booth.room.floor.number
        booth_name = booth.circle.name
        booth_room = booth.room.name

        initial_data = {
            'floor':request.GET.get('current_floor',''),
            'booth':booth_name
        }
        form = NavigationForm(initial = initial_data)


        if current_floor is not None:
            instructions['intro'].append(f"縺ゅ↑縺溘・迴ｾ蝨ｨ縺・ｋ髫主ｱ､縺ｯ{current_floor}髫弱〒縺・)
            instructions['intro'].append(f"{booth_name}縺ｮ繝悶・繧ｹ縺ｯ{destination_floor}髫弱↓縺ゅｊ縺ｾ縺・)

        else:
            instructions['intro'].append(f"{booth_name}縺ｮ繝悶・繧ｹ縺ｯ{destination_floor}髫弱↓縺ゅｊ縺ｾ縺・)
            instructions['intro'].append("繝悶・繧ｹ縺ｮ菴咲ｽｮ逕ｻ蜒上ｒ縺皮｢ｺ隱阪￥縺縺輔＞縲ら樟蝨ｨ蝨ｰ繧貞・蜉帙☆繧九％縺ｨ縺ｧ譯亥・繧帝幕蟋九〒縺阪∪縺・)
        
        short_elevator_url = None
        long_elevator_url  =None
        if current_floor is not None :
            floor_diff = abs(destination_floor - current_floor)
                #蜷後§髫弱↓縺・ｋ蝣ｴ蜷医・逕ｻ蜒・               
            if current_floor == destination_floor:
                instructions['floor_move'].append("縺ゅ↑縺溘・縺吶〒縺ｫ逶ｮ逧・・髫弱↓縺・∪縺・)
                #1髫弱°繧・髫弱∪縺ｧ荳翫′繧区凾縲∽ｽ主ｱ､髫弱・繧ｨ繝ｬ繝吶・繧ｿ繝ｼ縺ｫ隱伜ｰ弱☆繧・
            elif current_floor == 1 and destination_floor == 4:
                instructions['floor_move'].append(f"{destination_floor}髫弱∪縺ｧ遘ｻ蜍輔＠縺ｦ縺上□縺輔＞")
                instructions['floor_move'].append(f"菴主ｱ､髫弱↓縺ゅｋ繧ｨ繝ｬ繝吶・繧ｿ繝ｼ繧呈耳螂ｨ縺励∪縺・)

                short_elevator_instance = current_floor_instance.connectors.filter(name__icontains= "short").first()
                if short_elevator_instance and short_elevator_instance.test_image:
                    instructions['floor_move'].append('test')
                    short_elevator_url = short_elevator_instance.test_image.url
                    
                else:
                    short_elevator_url = None
                #4髫惹ｻ･荳翫・荳翫′繧翫・蝣ｴ蜷医・縲∽ｸ雁ｱ､髫弱∈縺ｮ繧ｨ繝ｬ繝吶・繧ｿ繝ｼ縺ｫ隱伜ｰ弱☆繧・
            elif floor_diff >= 4:
                instructions['floor_move'].append(f"{destination_floor}髫弱∪縺ｧ遘ｻ蜍輔＠縺ｦ縺上□縺輔＞")
                instructions['floor_move'].append(f"荳雁ｱ､髫弱↓郢九′繧九お繝ｬ繝吶・繧ｿ繝ｼ繧呈耳螂ｨ縺励∪縺・)
                    
                long_elevator_instance = current_floor_instance.connectors.filter(name__icontains= "long").first()
                if long_elevator_instance and long_elevator_instance.test_image:
                    long_elevator_url = long_elevator_instance.test_image.url
                else:
                    long_elevator_url = None

            #谿九ｊ縺ｯ繧ｨ繧ｹ繧ｫ繝ｬ繝ｼ繧ｿ繝ｼ縺ｪ縺ｩ縺ｧ荳翫′縺｣縺ｦ繧ゅｉ縺・ゅお繧ｹ繧ｫ繝ｬ繝ｼ繧ｿ繝ｼ縺ｪ縺ｩ縺ｮ蝣ｴ謇縺ｯ閾ｪ譏弱↑縺ｮ縺ｧ逕ｻ蜒上ｂ貂｡縺輔↑縺・
            else:
                instructions['floor_move'].append(f"繧ｨ繧ｹ繧ｫ繝ｬ繝ｼ繧ｿ繝ｼ縺ｪ縺ｩ縺ｧ{destination_floor}髫弱∪縺ｧ遘ｻ蜍輔＠縺ｦ縺上□縺輔＞")

        
        instructions['room_guide'].append(f"逶ｮ逧・・繝悶・繧ｹ縺ｯ{booth_room}縺ｫ縺ゅｊ縺ｾ縺吶・)
        room_image_url = booth.room.test_image.url if booth.room.test_image else None



        return render(request, 'map/result.html', {
            'form': form,
            'instructions': instructions,
            'room_image_url':room_image_url,
            'short_elevator_url':short_elevator_url,
            'long_elevator_url':long_elevator_url
            })
    
            
        

            



        

        # instructions = []  # 縺ｾ縺夂ｩｺ縺ｮ繝ｪ繧ｹ繝医ｒ蛻晄悄蛹・
        # if current_floor is not None:
        #     destination_floor = booth.room.floor.number
        #     booth_name = booth.circle.name
        #     instructions.append(f"{booth_name}縺ｮ繝悶・繧ｹ縺ｯ{destination_floor}髫弱↓縺ゅｊ縺ｾ縺・)
            
        #     if current_floor == destination_floor:
        #         instructions.append("縺ゅ↑縺溘・譌｢縺ｫ繝悶・繧ｹ縺後≠繧矩嚴縺ｫ縺・∪縺吶・)
        #         instructions.append(f"逶ｮ逧・・繝悶・繧ｹ縺ｯ{booth.room.name}縺ｫ縺ゅｊ縺ｾ縺・)
        #     else:
        #         floor_diff = abs(destination_floor - current_floor)
        #         if current_floor < destination_floor:
        #             instructions.append(f"縺ゅ↑縺溘・迴ｾ蝨ｨ{current_floor}髫弱↓縺・∪縺吶・floor_diff}髫惹ｸ翫′繧句ｿ・ｦ√′縺ゅｊ縺ｾ縺吶・)
        #         else:
        #             instructions.append(f"縺ゅ↑縺溘・迴ｾ蝨ｨ{current_floor}髫弱↓縺・∪縺吶・floor_diff}髫惹ｸ九′繧句ｿ・ｦ√′縺ゅｊ縺ｾ縺吶・)
        #         instructions.append(f"逶ｮ逧・・繝悶・繧ｹ縺ｯ{booth.room.name}縺ｫ縺ゅｊ縺ｾ縺・)
        #     destination = instructions
        #     room_image_url = booth.room.test_image.url if booth.room.test_image else None
        # else:
        #     # booth_id縺縺代′貂｡縺輔ｌ縺溷ｴ蜷医・蜃ｦ逅・ｼ井ｾ具ｼ夂判蜒上・縺ｿ陦ｨ遉ｺ・・
        #     destination_floor = booth.room.floor.number
        #     booth_name = booth.circle.name
        #     instructions.append(f"{booth_name}縺ｮ繝悶・繧ｹ縺ｯ{destination_floor}髫弱↓縺ゅｊ縺ｾ縺・)
        #     instructions.append("繝悶・繧ｹ縺ｮ菴咲ｽｮ逕ｻ蜒上ｒ縺皮｢ｺ隱阪￥縺縺輔＞縲ら樟蝨ｨ蝨ｰ繧貞・蜉帙☆繧九％縺ｨ縺ｧ譯亥・繧帝幕蟋九〒縺阪∪縺・)
        #     destination = instructions
        #     room_image_url = booth.room.test_image.url if booth.room.test_image else None
        

    def post(self, request):
        form = NavigationForm(request.POST)
        if form.is_valid():
            current_charfloor = form.cleaned_data['floor']
            current_floor = int(current_charfloor)
            booth_query = form.cleaned_data['booth']
            booth_instance = Booth.objects.filter(circle__name__icontains=booth_query).first()
                
            if not booth_instance:
                context = {
                    'form': form,
                    'destination': "謖・ｮ壹＆繧後◆繝悶・繧ｹ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ縺ｧ縺励◆",
                }
                return render(request, 'map/index.html', context)
            else:
                url = reverse('map:result') + f'?booth_id={booth_instance.id}&current_floor={current_floor}'
                return redirect(url)
        return render(request, 'map/index.html', {'form': form})
    
   # AJAX縺ｫ繧医ｋ繧ｪ繝ｼ繝医さ繝ｳ繝励Μ繝ｼ繝医・縺溘ａ縺ｮ繝薙Η繝ｼ
def booth_autocomplete(request):
    form = NavigationForm(request.POST)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        booth_query = request.GET.get('term', '')
        #booth縺ｮinstance縺御ｸ弱∴繧峨ｌ繧・
        booth_js_instance = Booth.objects.filter(
            circle__name__icontains=booth_query)[:10]
        # instance縺九ｉ蛟呵｣懊→縺励※繝悶・繧ｹ蜷阪・繝ｪ繧ｹ繝医ｒ霑斐☆
        results = list(booth_js_instance.values_list('circle__name', flat=True))

        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

class TestView(View):
    def get (self, request, **kwargs):
        context = {'form' : NavigationForm()}
        return render(request, 'map/test.html', context)
        # #QR繧ｳ繝ｼ繝峨・id(url縺九ｉ貂｡縺輔ｌ繧・繧貞女縺大叙縺｣縺ｦmodel縺ｫ縺昴・QR繧ｳ繝ｼ繝峨・髢ｲ隕ｧ謨ｰ繧定ｨ域ｸｬ縺吶ｋ縲・
        # #縺ｩ縺ｮQR繧ｳ繝ｼ繝峨°繧峨・繝ｼ繧ｸ繧帝夢隕ｧ縺輔ｌ縺ｦ縺・ｋ縺九′蛻・°繧九・
        # qr_id = self.kwargs.get('qr_id')
        # if qr_id is not None:
        #     qr_view, created = QRViewCount.objects.get_or_create(qr_id=qr_id)
        #     qr_view.view_count += 1
        #     qr_view.save()
        # else: pass



        # #url縺ｫfloor縺後≠繧後・縺昴ｌ繧貞・譛溷､縺ｫ險ｭ螳・
        # #url縺ｫfloor縺後≠繧九→縺・≧縺薙→縺ｯQR繧ｳ繝ｼ繝峨°繧峨い繧ｯ繧ｻ繧ｹ縺励※縺・ｋ縺ｨ縺・≧縺薙→縺ｫ縺ｪ繧・
        # initial_floor = request.GET.get('floor_id')
        # if initial_floor is not None:
        #     try:
        #         initial_floor = int(initial_floor)
        #     except ValueError:
        #         initial_floor = None
      

        # #url縺ｫbooth_id縺後≠繧後・縺昴ｌ繧貞・譛溷､縺ｫ險ｭ螳・   
        # #TODO:蜷・ooth繧帝夢隕ｧ縺ｧ縺阪ｋ縺ｨ縺薙ｍ縺九ｉ逶ｮ逧・慍縺ｫ險ｭ螳壹〒縺阪ｋ繝ｪ繝ｳ繧ｯ繧剃ｽ懊ｋ縺九ｂ縺励ｌ縺ｪ縺・・縺ｧ縲∽ｸ蠢彙ooth_id縺蛍rl縺ｫ蜈･縺｣縺ｦ縺・ｋ繝代ち繝ｼ繝ｳ繧定ｨ倩ｿｰ縺励※縺翫￥
        # #TODO: booth_id縺九ｉbooth_name縺ｫ縺吶ｋ繧ｳ繝ｼ繝峨ｒ菴懊ｋ
        # initial_booth = request.GET.get('booth_id')
        # if initial_booth is not None:
        #     try: 
        #         initial_booth = int (initial_booth)
        #     except ValueError:
        #         initial_booth = None
        # form = NavigationForm(initial={'current_floor': initial_floor, 'current_booth':initial_booth})
        # return render(request, 'map/navigation.html', {'form': form})



    def post (self, request, *args, **kwargs):

        form = NavigationForm(request.POST)

        #destination縺ｫ隱ｬ譏弱ｒ蜈･繧後※縺・￥縲よ怙蛻昴↓陦ｨ遉ｺ縺励◆譎ゅ↓蝠城｡後′縺ゅｋ縺ｨ雖後↑縺ｮ縺ｧ譏守､ｺ逧・↓None繧剃ｻ｣蜈･
        destination = None

        #form縺九ｉ髫弱→逶ｮ逧・慍繧定ｲｰ縺｣縺ｦ縺・ｋ縲・
        #form縺ｯbooth縺ｮmodel縺九ｉ逶ｮ逧・慍繧定ｨｭ螳壹☆繧九ｈ縺・↓縺ｪ縺｣縺ｦ縺・ｋ縺溘ａ縲‘rror縺ｯ縺ｻ縺ｨ繧薙←襍ｷ縺阪↑縺・・縺壹□縺後∽ｸ蠢彳xcept縺吶ｋ縲・
        if form.is_valid():
            current_floor = form.cleaned_data['floor']
            booth_name = form.cleaned_data['booth']

            try:
                booth = Booth.objects.filter(name__icontains=booth_name).first()
                if not booth:
                    raise Booth.DoesNotExist
            except Booth.DoesNotExist:
                destination = "謖・ｮ壹＆繧後◆繝悶・繧ｹ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ縺ｧ縺励◆"

            else:
                #逶ｮ逧・・booth縺ｮ髫弱′縺ｩ縺薙↓縺ゅｋ縺ｮ縺九ｒ蜿門ｾ・
                destination_floor = booth.room.floor.number
            
                #隱ｬ譏取枚繧堤ｩｺ繝ｪ繧ｹ繝医〒螳夂ｾｩ縲る嚴繧・岼逧・慍縺ｫ蠢懊§縺ｦ縲∬ｪｬ譏取枚繧偵％縺薙↓蜈･繧後※縺・￥
                instructions = []
                instructions.append(f"逶ｮ逧・・繝悶・繧ｹ縺ｯ{destination_floor}髫弱↓縺ゅｊ縺ｾ縺吶・)

                #迴ｾ蝨ｨ蝨ｰ縺ｨ髫主ｱ､縺悟酔縺倥□縺｣縺溘ｉ縲√☆縺舌↓蝣ｴ謇縺ｮ隱ｬ譏弱ｒ縺吶ｋ
                if current_floor == destination_floor:
                    instructions.append("縺ゅ↑縺溘・譌｢縺ｫ繝悶・繧ｹ縺後≠繧矩嚴縺ｫ縺・∪縺吶・)
                    instructions.append(f"逶ｮ逧・・繝悶・繧ｹ縺ｯ {booth.room.name} 縺ｫ縺ゅｊ縺ｾ縺吶・)
                    destination = instructions
                    return render(request, 'map/index.html', {'form':form, 'destination':destination})
            
                #迴ｾ蝨ｨ蝨ｰ縺ｨ髫主ｱ､縺碁＆縺｣縺溘ｉ縲・嚴螻､縺ｮ遘ｻ蜍輔ｒ隱ｬ譏弱☆繧・
                else:
                    floor_diff = abs(destination_floor - current_floor)
                    if current_floor < destination_floor:
                        instructions.append(f"縺ゅ↑縺溘・迴ｾ蝨ｨ{current_floor}髫弱↓縺・∪縺吶・floor_diff}髫惹ｸ翫′繧句ｿ・ｦ√′縺ゅｊ縺ｾ縺吶・)
                    else:
                        instructions.append(f"縺ゅ↑縺溘・迴ｾ蝨ｨ{current_floor}髫弱↓縺・∪縺吶・floor_diff}髫惹ｸ九′繧句ｿ・ｦ√′縺ゅｊ縺ｾ縺吶・)
                    instructions.append(f"逶ｮ逧・・繝悶・繧ｹ縺ｯ{booth.room.name}縺ｫ縺ゅｊ縺ｾ縺吶・)
                    destination = instructions
                return render(request, 'map/index.html', {'form':form, 'destination':destination})
        

