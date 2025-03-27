from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length= 50,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"


class Circle(models.Model):
    name = models.CharField(
        max_length= 50,
        null=True,
        blank=True 
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


#髫弱ｒ驛ｨ螻・謨吝ｮ､)縺ｫ邏舌▼縺代∵蕗螳､繧達ooth縺ｫ邏舌▼縺代ｋ縲・
#菴暮嚴縺九ｒ蠕後・險育ｮ励↓菴ｿ逕ｨ縺吶ｋ縺溘ａ縲：loor縺ｯint縺ｫ縺吶ｋ縲・
class Floor(models.Model):
    number = models.IntegerField(
        default=0
    )


    def __str__(self):
        return f"Floor{self.number}"

class Connector(models.Model):
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='connectors'           

    )
    
    name = models.CharField(
        null=True,
        blank=True   
    )

    test_image = models.ImageField(
        verbose_name="繝・せ繝育判蜒・,
        upload_to='map/test_images',
        null=True,
        blank=True
    )


    def __str__(self):
        return f"{self.name}"

    

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

    #譁・ｭ励′蜈･縺｣縺溘□縺代・繝・せ繝育判蜒上ｒ蜈･繧後※縺翫￥縺溘ａ縺ｮmodel
    test_image = models.ImageField(
        verbose_name="繝・せ繝育判蜒・,
        upload_to='map/test_images',
        null=True,
        blank=True
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

    circle = models.ForeignKey(
        Circle,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.circle} in {self.room}"
    

class QRViewCount(models.Model):
    qr_id = models.IntegerField(unique=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"QR {self.qr_id}: {self.view_count} views"