from django.urls import path
from . import views as v

app_name = "map"
urlpatterns = [
    path('result/', v.ResultView.as_view(), name='result'),
    path('', v.IndexView.as_view(), name="index"),
    path('autocomplete/', v.booth_autocomplete, name='booth-autocomplete'),
    path('test/', v.TestView.as_view(), name="test")
]