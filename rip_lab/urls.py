

from django.contrib import admin
from django.urls import path	
from rip import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ships/',views.ships),
    path('ship/<int:ship_id>/',views.ship),
    path('delete_ship/<int:ship_id>/',views.delete_ship)
]
