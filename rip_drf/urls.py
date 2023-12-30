from django.contrib import admin
from rip import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'classes_of_ships', views.get_all_classes_of_ships, name='get_all_classes_of_ships'),
    path(r'classes_of_ships/add/', views.post_add_class_of_ships, name='post_add_class_of_ships'),
    path(r'classes_of_ships/<int:ship_id>/', views.get_one_class_of_ships, name='get_one_class_of_ships'),
    path(r'classes_of_ships/<int:ship_id>/change/', views.change_class_of_ship, name='change_class_of_ship'),
    path(r'classes_of_ships/<int:ship_id>/delete/', views.delete_class_of_ship, name='delete_class_of_ship'),
    path(r'classes_of_ships/<int:ship_id>/add_to_order/', views.add_class_of_ship_to_order, name='add_class_of_ship_to_order'),


    path(r'orders/', views.get_all_orders, name='get_all_orders'),
    path(r'orders/form_order/', views.form_order, name='form_order'),
    path(r'orders/delete_order/', views.delete_order, name='delete_order'),
    path(r'orders/<int:order_id>/', views.get_one_order, name='get_one_order'),
    path(r'orders/<int:order_id>/approve_order/', views.approve_order, name='approve_order'),
    path(r'orders/<int:order_id>/decline_order/', views.decline_order, name='decline_order'),

    path(r'links/delete_class_from_order/<int:ship_id>/', views.delete_class_from_order, name='delete_class_from_order'),
    path(r'links/change_imo/<int:ship_id>/', views.change_imo, name='change_imo'),

    path('admin/', admin.site.urls),
]