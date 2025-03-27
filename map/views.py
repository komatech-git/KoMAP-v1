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
        # boothをランダムに3件表示する
        booths = Booth.objects.order_by('?')[:3]
        
        booth_info = []
        for booth in booths:
            circle_name = booth.circle.name if booth.circle else "未設宁E
            room_name = booth.room.name if booth.room else "未設宁E
            # 結果ペ�EジのURLにbooth_idをクエリパラメータとして付丁E
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
                    'destination': "持E��されたブ�Eスが見つかりませんでした",
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
            destination = "忁E��な惁E��が見つかりませんでした。�E度入力してください"
            return render(request, 'map/index.html', {'form': form, 'destination': destination})
        
        try:
            booth = Booth.objects.get(pk=booth_id)
        except Booth.DoesNotExist:
            destination = "持E��されたブ�Eスが見つかりませんでした"
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
            instructions['intro'].append(f"あなた�E現在ぁE��階層は{current_floor}階でぁE)
            instructions['intro'].append(f"{booth_name}のブ�Eスは{destination_floor}階にありまぁE)

        else:
            instructions['intro'].append(f"{booth_name}のブ�Eスは{destination_floor}階にありまぁE)
            instructions['intro'].append("ブ�Eスの位置画像をご確認ください。現在地を�E力することで案�Eを開始できまぁE)
        
        short_elevator_url = None
        long_elevator_url  =None
        if current_floor is not None :
            floor_diff = abs(destination_floor - current_floor)
                #同じ階にぁE��場合�E画僁E               
            if current_floor == destination_floor:
                instructions['floor_move'].append("あなた�Eすでに目皁E�E階にぁE��ぁE)
                #1階かめE階まで上がる時、低層階�Eエレベ�Eターに誘導すめE
            elif current_floor == 1 and destination_floor == 4:
                instructions['floor_move'].append(f"{destination_floor}階まで移動してください")
                instructions['floor_move'].append(f"低層階にあるエレベ�Eターを推奨しまぁE)

                short_elevator_instance = current_floor_instance.connectors.filter(name__icontains= "short").first()
                if short_elevator_instance and short_elevator_instance.test_image:
                    instructions['floor_move'].append('test')
                    short_elevator_url = short_elevator_instance.test_image.url
                    
                else:
                    short_elevator_url = None
                #4階以上�E上がり�E場合�E、上層階へのエレベ�Eターに誘導すめE
            elif floor_diff >= 4:
                instructions['floor_move'].append(f"{destination_floor}階まで移動してください")
                instructions['floor_move'].append(f"上層階に繋がるエレベ�Eターを推奨しまぁE)
                    
                long_elevator_instance = current_floor_instance.connectors.filter(name__icontains= "long").first()
                if long_elevator_instance and long_elevator_instance.test_image:
                    long_elevator_url = long_elevator_instance.test_image.url
                else:
                    long_elevator_url = None

            #残りはエスカレーターなどで上がってもらぁE��エスカレーターなどの場所は自明なので画像も渡さなぁE
            else:
                instructions['floor_move'].append(f"エスカレーターなどで{destination_floor}階まで移動してください")

        
        instructions['room_guide'].append(f"目皁E�Eブ�Eスは{booth_room}にあります、E)
        room_image_url = booth.room.test_image.url if booth.room.test_image else None



        return render(request, 'map/result.html', {
            'form': form,
            'instructions': instructions,
            'room_image_url':room_image_url,
            'short_elevator_url':short_elevator_url,
            'long_elevator_url':long_elevator_url
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
                    'destination': "持E��されたブ�Eスが見つかりませんでした",
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
    def get (self, request, **kwargs):
        context = {'form' : NavigationForm()}
        return render(request, 'map/test.html', context)
        # #QRコード�Eid(urlから渡されめEを受け取ってmodelにそ�EQRコード�E閲覧数を計測する、E
        # #どのQRコードから�Eージを閲覧されてぁE��かが刁E��る、E
        # qr_id = self.kwargs.get('qr_id')
        # if qr_id is not None:
        #     qr_view, created = QRViewCount.objects.get_or_create(qr_id=qr_id)
        #     qr_view.view_count += 1
        #     qr_view.save()
        # else: pass



        # #urlにfloorがあれ�Eそれを�E期値に設宁E
        # #urlにfloorがあるとぁE��ことはQRコードからアクセスしてぁE��とぁE��ことになめE
        # initial_floor = request.GET.get('floor_id')
        # if initial_floor is not None:
        #     try:
        #         initial_floor = int(initial_floor)
        #     except ValueError:
        #         initial_floor = None
      

        # #urlにbooth_idがあれ�Eそれを�E期値に設宁E   
        # #TODO:吁Eoothを閲覧できるところから目皁E��に設定できるリンクを作るかもしれなぁE�Eで、一応booth_idがurlに入ってぁE��パターンを記述しておく
        # #TODO: booth_idからbooth_nameにするコードを作る
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

        #destinationに説明を入れてぁE��。最初に表示した時に問題があると嫌なので明示皁E��Noneを代入
        destination = None

        #formから階と目皁E��を貰ってぁE��、E
        #formはboothのmodelから目皁E��を設定するよぁE��なってぁE��ため、errorはほとんど起きなぁE�Eずだが、一応exceptする、E
        if form.is_valid():
            current_floor = form.cleaned_data['floor']
            booth_name = form.cleaned_data['booth']

            try:
                booth = Booth.objects.filter(name__icontains=booth_name).first()
                if not booth:
                    raise Booth.DoesNotExist
            except Booth.DoesNotExist:
                destination = "持E��されたブ�Eスが見つかりませんでした"

            else:
                #目皁E�Eboothの階がどこにあるのかを取征E
                destination_floor = booth.room.floor.number
            
                #説明文を空リストで定義。階めE��皁E��に応じて、説明文をここに入れてぁE��
                instructions = []
                instructions.append(f"目皁E�Eブ�Eスは{destination_floor}階にあります、E)

                #現在地と階層が同じだったら、すぐに場所の説明をする
                if current_floor == destination_floor:
                    instructions.append("あなた�E既にブ�Eスがある階にぁE��す、E)
                    instructions.append(f"目皁E�Eブ�Eスは {booth.room.name} にあります、E)
                    destination = instructions
                    return render(request, 'map/index.html', {'form':form, 'destination':destination})
            
                #現在地と階層が違ったら、E��層の移動を説明すめE
                else:
                    floor_diff = abs(destination_floor - current_floor)
                    if current_floor < destination_floor:
                        instructions.append(f"あなた�E現在{current_floor}階にぁE��す、Efloor_diff}階上がる忁E��があります、E)
                    else:
                        instructions.append(f"あなた�E現在{current_floor}階にぁE��す、Efloor_diff}階下がる忁E��があります、E)
                    instructions.append(f"目皁E�Eブ�Eスは{booth.room.name}にあります、E)
                    destination = instructions
                return render(request, 'map/index.html', {'form':form, 'destination':destination})
        

