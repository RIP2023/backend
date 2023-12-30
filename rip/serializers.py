from .models import Order,Class_of_Ship,Order_for_Ship, Custom_User
from rest_framework import serializers


class Order_Serializer(serializers.ModelSerializer):
    full_name_creator = serializers.SerializerMethodField()
    def get_full_name_creator(self, obj):
        return obj.creator.username 
    full_name_mod = serializers.SerializerMethodField()
    def get_full_name_mod(self, obj):
        try:
            return obj.moderator.username
        except:
            return ""
        
    class Meta:
        # Модель, которую мы сериализуем
        model = Order
        # Поля, которые мы сериализуем
        fields = ['order_id',"status", "start_date", "in_work", "end_date", "full_name_mod",'full_name_creator']



class Class_of_Ship_Serializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Class_of_Ship
        # Поля, которые мы сериализуем
        fields = ['ship_id','photo_data',"name", "type",'rang','stuff','project','description','status']
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 


class Order_for_Ship(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Order_for_Ship
        # Поля, которые мы сериализуем
        fields = ["ship_id", "order_id", "imo_of_ship"]

class Custom_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_User
        fields = ['username','email','password','is_manager']
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 