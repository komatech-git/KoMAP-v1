from django.contrib import admin
from .models import Booth, Room, Floor, QRViewCount, Circle

# Register your models here.

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(Booth)
admin.site.register(Room)
admin.site.register(Floor)
admin.site.register(QRViewCount)


