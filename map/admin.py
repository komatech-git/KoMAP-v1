from django.contrib import admin
from .models import Booth, Room, Floor, QRViewCount, Circle, Category

# Register your models here.

admin.site.register(Category)

class CircleCategoryFilter(admin.SimpleListFilter):
    title = 'category'
    parameter_name = 'circle_category'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        categories = set()
        # select_related("category") により、各 Circle の category を効率的に取得
        for circle in qs.select_related("category"):
            if circle.category:
                categories.add(circle.category)
        # それぞれの Category の id と名前を返す
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id=self.value())
        return queryset

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = (CircleCategoryFilter,)

class BoothRoomFloorFilter(admin.SimpleListFilter):
    title = '部屋の階'  # 管理画面に表示するフィルターのタイトル
    parameter_name = 'room_floor'  # URLでのパラメータ名

    def lookups(self, request, model_admin):
        # クエリセットから、Booth に紐づく Room の Floor を一意に取得
        floors = set()
        for booth in model_admin.get_queryset(request).select_related('room__floor'):
            if booth.room and booth.room.floor:
                floors.add(booth.room.floor)
        # (値, 表示名) のタプルのリストを返す
        return [(floor.id, str(floor)) for floor in floors]

    def queryset(self, request, queryset):
        if self.value():
            # Booth の room__floor の id でフィルタする
            return queryset.filter(room__floor__id=self.value())
        return queryset

@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ('circle', 'room')
    list_filter = (BoothRoomFloorFilter,)

admin.site.register(Room)
admin.site.register(Floor)
admin.site.register(QRViewCount)


