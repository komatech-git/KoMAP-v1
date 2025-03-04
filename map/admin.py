from django.contrib import admin
from .models import Booth, Room, Floor, QRViewCount

# Register your models here.

admin.site.register(Booth)
admin.site.register(Room)
admin.site.register(Floor)
admin.site.register(QRViewCount)


