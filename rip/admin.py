from django.contrib import admin
from .models import *
from django import forms
import base64

# Register your models here.

admin.site.register(Custom_User)
admin.site.register(Order)
admin.site.register(Order_for_Ship)

class BinaryField(forms.FileField):
    def to_python(self, data):
        data = super().to_python(data)
        if data:
            data = base64.b64encode(data.read()).decode('ascii')
        return data

class BinaryFileInputAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BinaryField: {'form_class': BinaryField},
    }
admin.site.register(Class_of_Ship, BinaryFileInputAdmin)