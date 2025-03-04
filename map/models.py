from django.db import models

# Create your models here.

#階を部屋(教室)に紐づけ、教室をBoothに紐づける。
#何階かを後の計算に使用するため、Floorはintにする。
class Floor(models.Model):
    number = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f"Floor{self.number}"

class Room(models.Model):
    floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

 
    name = models.CharField(
        max_length=100,default="default"
    )

    def __str__(self):
        return f"Room {self.name} on {self.floor}"
    

class Booth(models.Model):
    room = models.ForeignKey(
        Room, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
    )

    unique_id = models.IntegerField(
        unique=True
    )

    def __str__(self):
        return f"{self.name} in {self.room}"
    

class QRViewCount(models.Model):
    qr_id = models.IntegerField(unique=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"QR {self.qr_id}: {self.view_count} views"