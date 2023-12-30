from .models import Order,Class_of_Ship,Order_for_Ship
from rest_framework import serializers


class Order_Serializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Order
        # Поля, которые мы сериализуем
        fields = ['order_id',"status", "start_date", "in_work", "end_date", "moderator",'creator']



class Class_of_Ship_Serializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Class_of_Ship
        # Поля, которые мы сериализуем
        fields = ['ship_id','photo_data',"name", "type",'rang','stuff','project','description','status']


class Order_for_Ship(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Order_for_Ship
        # Поля, которые мы сериализуем
        fields = ["ship_id", "order_id", "imo_of_ship"]