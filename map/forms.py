# forms.py
from django import forms
from .models import Floor

class NavigationForm(forms.Form):
    # ユーザーが現在ぁE��階を入劁E
    floor = forms.ChoiceField(
        label="現在の階",
        choices=[], 
        )
    # ユーザーが目皁E��するブ�Eス名を入劁E
    booth = forms.CharField(label="目的のブース", max_length=100)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['floor'].choices= [(f.id, f.number) for f in Floor.objects.order_by('number')]