# forms.py
from django import forms
from .models import Floor

class NavigationForm(forms.Form):
    # 繝ｦ繝ｼ繧ｶ繝ｼ縺檎樟蝨ｨ縺・ｋ髫弱ｒ蜈･蜉・
    floor = forms.ChoiceField(
        label="迴ｾ蝨ｨ縺ｮ髫・,
        choices=[], 
        )
    # 繝ｦ繝ｼ繧ｶ繝ｼ縺檎岼逧・→縺吶ｋ繝悶・繧ｹ蜷阪ｒ蜈･蜉・
    booth = forms.CharField(label="逶ｮ逧・・繝悶・繧ｹ", max_length=100)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['floor'].choices= [(f.id, f.number) for f in Floor.objects.order_by('number')]