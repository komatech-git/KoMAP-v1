# forms.py
from django import forms
from .models import Floor

class NavigationForm(forms.Form):
    # ユーザーが現在いる階を入力
    floor = forms.ChoiceField(
        label="現在の階",
        choices=[], 
        )
    # ユーザーが目的とするブース名を入力
    booth = forms.CharField(label="目的のブース", max_length=100)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['floor'].choices= [(f.id, f.number) for f in Floor.objects.all()]