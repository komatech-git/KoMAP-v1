from django.urls import path
from . import views as v

app_name = "map"
urlpatterns = [
    path('',v.MapView.as_view(), name='index'),
    path('api/booth-suggestions/', v.booth_suggestions, name='booth_suggestions'),

]