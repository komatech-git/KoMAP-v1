from django.shortcuts import render
from django.views import View
from . models import QRViewCount, Booth
from django.http import JsonResponse
from .forms import NavigationForm
# Create your views here.

class MapView(View):
    def get (self, request, **kwargs):
        context = {'form' : NavigationForm()}
        return render(request, 'map/index.html', context)
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

#APIでboothの検索候補を返す
def booth_suggestions(request):
    q = request.GET.get('q','')
    suggestions = []
    if q:
        booths = Booth.objects.filter(name__icontains=q)[:5]
        suggestions = [booth.name for booth in booths]
    return JsonResponse({'suggestions': suggestions})
        


