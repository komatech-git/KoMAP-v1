# forms.py
from django import forms

class NavigationForm(forms.Form):
    # ユーザーが現在いる階を入力
    floor = forms.IntegerField(label="現在の階")
    # ユーザーが目的とするブース名を入力
    booth = forms.CharField(label="目的のブース", max_length=100)

    #TODO: formに改良が必要。modelからboothが検索欄に表示されるようにするべき