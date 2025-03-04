from django.urls import path
from .views import TestView

app_name = "festival_p1"
urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
]