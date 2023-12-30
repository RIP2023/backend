from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Custom_User)
admin.site.register(Order)
admin.site.register(Ship)
admin.site.register(Order_for_Ship)
