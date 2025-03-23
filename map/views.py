from django.shortcuts import render, redirect
from django.views import View
from . models import QRViewCount, Booth
from django.urls import reverse
from django.http import JsonResponse
from .forms import NavigationForm
import datetime
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
            # 結果ページのURLにbooth_idをクエリパラメータとして付与
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
                    'destination': "指定されたブースが見つかりませんでした",
                }
                return render(request, 'map/index.html', context)
            else:
                # URLクエリパラメータとしてbooth_idとcurrent_floorを渡す
                url = reverse('map:result') + f'?booth_id={booth_instance.id}&current_floor={current_floor}'
                return redirect(url)
        return render(request, 'map/index.html', {'form': form})


class ResultView(View):
    def get(self, request, **kwargs):
        form = NavigationForm()
        # セッションではなくGETパラメータから値を取得
        booth_id = request.GET.get('booth_id')
        current_floor = request.GET.get('current_floor')
        
        # current_floorが文字列で渡されるので、数値に変換（変換できなければNone）
        if current_floor is not None:
            try:
                current_floor = int(current_floor)
            except ValueError:
                current_floor = None
        
        if booth_id is None:
            destination = "必要な情報が見つかりませんでした。再度入力してください"
            return render(request, 'map/index.html', {'form': form, 'destination': destination})
        
        try:
            booth = Booth.objects.get(pk=booth_id)
        except Booth.DoesNotExist:
            destination = "指定されたブースが見つかりませんでした"
            return render(request, 'map/index.html', {'form': form, 'destination': destination})
        
        instructions = []  # まず空のリストを初期化
        if current_floor is not None:
            destination_floor = booth.room.floor.number
            booth_name = booth.circle.name
            instructions.append(f"{booth_name}のブースは{destination_floor}階にあります")
            
            if current_floor == destination_floor:
                instructions.append("あなたは既にブースがある階にいます。")
                instructions.append(f"目的のブースは{booth.room.name}にあります")
            else:
                floor_diff = abs(destination_floor - current_floor)
                if current_floor < destination_floor:
                    instructions.append(f"あなたは現在{current_floor}階にいます。{floor_diff}階上がる必要があります。")
                else:
                    instructions.append(f"あなたは現在{current_floor}階にいます。{floor_diff}階下がる必要があります。")
                instructions.append(f"目的のブースは{booth.room.name}にあります")
            destination = instructions
            room_image_url = booth.room.test_image.url if booth.room.test_image else None
        else:
            # booth_idだけが渡された場合の処理（例：画像のみ表示）
            destination_floor = booth.room.floor.number
            booth_name = booth.circle.name
            instructions.append(f"{booth_name}のブースは{destination_floor}階にあります")
            instructions.append("ブースの位置画像をご確認ください。現在地を入力することで案内を開始できます")
            destination = instructions
            room_image_url = booth.room.test_image.url if booth.room.test_image else None
        
        return render(request, 'map/result.html', {
            'form': form,
            'destination': destination,
            'room_image_url': room_image_url,
        })
    
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
    
   # AJAXによるオートコンプリートのためのビュー
def booth_autocomplete(request):
    form = NavigationForm(request.POST)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        booth_query = request.GET.get('term', '')
        #boothのinstanceが与えられる
        booth_js_instance = Booth.objects.filter(
            circle__name__icontains=booth_query)[:10]
        # instanceから候補としてブース名のリストを返す
        results = list(booth_js_instance.values_list('circle__name', flat=True))

        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

class TestView(View):
    def get (self, request, **kwargs):
        context = {'form' : NavigationForm()}
        return render(request, 'map/test.html', context)
        # #QRコードのid(urlから渡される)を受け取ってmodelにそのQRコードの閲覧数を計測する。
        # #どのQRコードからページを閲覧されているかが分かる。
        # qr_id = self.kwargs.get('qr_id')
        # if qr_id is not None:
        #     qr_view, created = QRViewCount.objects.get_or_create(qr_id=qr_id)
        #     qr_view.view_count += 1
        #     qr_view.save()
        # else: pass



        # #urlにfloorがあればそれを初期値に設定
        # #urlにfloorがあるということはQRコードからアクセスしているということになる
        # initial_floor = request.GET.get('floor_id')
        # if initial_floor is not None:
        #     try:
        #         initial_floor = int(initial_floor)
        #     except ValueError:
        #         initial_floor = None
      

        # #urlにbooth_idがあればそれを初期値に設定    
        # #TODO:各boothを閲覧できるところから目的地に設定できるリンクを作るかもしれないので、一応booth_idがurlに入っているパターンを記述しておく
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

        #destinationに説明を入れていく。最初に表示した時に問題があると嫌なので明示的にNoneを代入
        destination = None

        #formから階と目的地を貰っている。
        #formはboothのmodelから目的地を設定するようになっているため、errorはほとんど起きないはずだが、一応exceptする。
        if form.is_valid():
            current_floor = form.cleaned_data['floor']
            booth_name = form.cleaned_data['booth']

            try:
                booth = Booth.objects.filter(name__icontains=booth_name).first()
                if not booth:
                    raise Booth.DoesNotExist
            except Booth.DoesNotExist:
                destination = "指定されたブースが見つかりませんでした"

            else:
                #目的のboothの階がどこにあるのかを取得
                destination_floor = booth.room.floor.number
            
                #説明文を空リストで定義。階や目的地に応じて、説明文をここに入れていく
                instructions = []
                instructions.append(f"目的のブースは{destination_floor}階にあります。")

                #現在地と階層が同じだったら、すぐに場所の説明をする
                if current_floor == destination_floor:
                    instructions.append("あなたは既にブースがある階にいます。")
                    instructions.append(f"目的のブースは {booth.room.name} にあります。")
                    destination = instructions
                    return render(request, 'map/index.html', {'form':form, 'destination':destination})
            
                #現在地と階層が違ったら、階層の移動を説明する
                else:
                    floor_diff = abs(destination_floor - current_floor)
                    if current_floor < destination_floor:
                        instructions.append(f"あなたは現在{current_floor}階にいます。{floor_diff}階上がる必要があります。")
                    else:
                        instructions.append(f"あなたは現在{current_floor}階にいます。{floor_diff}階下がる必要があります。")
                    instructions.append(f"目的のブースは{booth.room.name}にあります。")
                    destination = instructions
                return render(request, 'map/index.html', {'form':form, 'destination':destination})
        


