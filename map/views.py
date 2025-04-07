import os 
from django.shortcuts import render, redirect
from django.views import View
from . models import QRViewCount, Booth, Floor
from django.urls import reverse
from django.http import JsonResponse
from .forms import NavigationForm
from django.conf import settings
import datetime
from urllib.parse import urlencode
# Create your views here.

class IndexView(View):
    def get(self, request):
        form = NavigationForm()
        # boothをランダムに3件表示する
        booths = Booth.objects.order_by('?')[:3]
        
        booth_info = []
        for booth in booths:
            circle_name = booth.circle.name if booth.circle else "未設定"
            room_name = booth.room.name if booth.room else "未設定"
            booth_floor = booth.room.floor.number if booth.room else "未設定"
            # 結果ペ�EジのURLにbooth_idをクエリパラメータとして付丁E
            url = reverse('map:result') + f'?booth_id={booth.id}'
            booth_info.append({
                "circle_name": circle_name,
                "room_name": room_name,
                "booth_floor": booth_floor,
                "url":url,
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
                    'destination': "指定されたブースが見つかりませんでした",
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
        
        # current_floorが文字�Eで渡される�Eで、数値に変換�E�変換できなければNone�E�E
        if current_floor is not None:
            try:
                current_floor = int(current_floor)
                current_floor_instance = Floor.objects.get(number=current_floor)
            except ValueError:
                current_floor = None
        
        if booth_id is None:
            destination = "指定されたブースIDが不適切です"
            return render(request, 'map/index.html', {'form': form, 'destination': destination})
        
        try:
            booth = Booth.objects.get(pk=booth_id)
        except Booth.DoesNotExist:
            destination = "指定されたブースが検索できませんでした"
            return render(request, 'map/index.html', {'form': form, 'destination': destination})
        
        instructions = {
            'intro':[],
            'floor_move':[],
            'room_guide':[],
            'room_floor':[],
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
            instructions['intro'].append(f"あなたが現在いる階層は{current_floor}階です")
            instructions['intro'].append(f"{booth_name}のブースは{destination_floor}階にあります")

        else:
            instructions['intro'].append(f"{booth_name}のブースは{destination_floor}階にあります")
            instructions['intro'].append("ブースの位置画像をご確認ください。現在地を入力することで案内を開始できます")
        

        if current_floor is not None :
            floor_diff = abs(destination_floor - current_floor)
                #同じ階にぁE��場合�E画僁E               
            if current_floor == destination_floor:
                instructions['floor_move'].append("あなたはすでに目的の階層にいます")
            else: 
                instructions['floor_move'].append(f"{destination_floor}階まで移動してください")
            
            # if destination_floor > current_floor:
            #     instructions['floor_move'].append(f"あなたは{floor_diff}階上がる必要があります")
            # elif destination_floor < current_floor:
            #     instructions['floor_move'].append(f"あなたは{floor_diff}階下がる必要があります")

        
        instructions['room_guide'].append(f"目的のブースは{booth_room}にあります")
        room_image_url = booth.room.test_image.url if booth.room.test_image else None
        floor_svg = booth.room.floor.svg_text if booth.room.floor.svg_text else None



        return render(request, 'map/result.html', {
            'form': form,
            'instructions': instructions,
            'floor_svg':floor_svg,
            'room_image_url':room_image_url,
            'booth_room':booth_room,
            })
    
            
        

            



        

        # instructions = []  # まず空のリストを初期匁E
        # if current_floor is not None:
        #     destination_floor = booth.room.floor.number
        #     booth_name = booth.circle.name
        #     instructions.append(f"{booth_name}のブ�Eスは{destination_floor}階にありまぁE)
            
        #     if current_floor == destination_floor:
        #         instructions.append("あなた�E既にブ�Eスがある階にぁE��す、E)
        #         instructions.append(f"目皁E�Eブ�Eスは{booth.room.name}にありまぁE)
        #     else:
        #         floor_diff = abs(destination_floor - current_floor)
        #         if current_floor < destination_floor:
        #             instructions.append(f"あなた�E現在{current_floor}階にぁE��す、Efloor_diff}階上がる忁E��があります、E)
        #         else:
        #             instructions.append(f"あなた�E現在{current_floor}階にぁE��す、Efloor_diff}階下がる忁E��があります、E)
        #         instructions.append(f"目皁E�Eブ�Eスは{booth.room.name}にありまぁE)
        #     destination = instructions
        #     room_image_url = booth.room.test_image.url if booth.room.test_image else None
        # else:
        #     # booth_idだけが渡された場合�E処琁E��例：画像�Eみ表示�E�E
        #     destination_floor = booth.room.floor.number
        #     booth_name = booth.circle.name
        #     instructions.append(f"{booth_name}のブ�Eスは{destination_floor}階にありまぁE)
        #     instructions.append("ブ�Eスの位置画像をご確認ください。現在地を�E力することで案�Eを開始できまぁE)
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
                    'destination': "指定されたブースが見つかりませんでした",
                }
                return render(request, 'map/index.html', context)
            else:
                url = reverse('map:result') + f'?booth_id={booth_instance.id}&current_floor={current_floor}'
                return redirect(url)
        return render(request, 'map/index.html', {'form': form})
    
   # AJAXによるオートコンプリート�Eためのビュー
def booth_autocomplete(request):
    form = NavigationForm(request.POST)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        booth_query = request.GET.get('term', '')
        #boothのinstanceが与えられめE
        booth_js_instance = Booth.objects.filter(
            circle__name__icontains=booth_query)[:10]
        # instanceから候補としてブ�Eス名�Eリストを返す
        results = list(booth_js_instance.values_list('circle__name', flat=True))

        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

class TestView(View):
    def get(self, request, *args, **kwargs):
        # SVGファイルのパスを設定
        svg_file_path = os.path.join(settings.BASE_DIR, 'data', 'floor9_改良版.svg')
        try:
            with open(svg_file_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
        except Exception as e:
            svg_content = f'<p>SVGファイルの読み込みに失敗しました: {e}</p>'
        
        # テンプレートにsvgの内容をコンテキストとして渡す
        context = {
            'svg_content': svg_content,
        }
        return render(request, 'map/test.html', context)
