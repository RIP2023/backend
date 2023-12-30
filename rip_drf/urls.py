from django.contrib import admin
from rip import views
from django.urls import include, path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
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
    path(r'orders/<int:order_id>/approve_or_decline_order/', views.approve_or_decline_order, name='approve_or_decline_order'),

    path(r'account/login/', views.authorize, name='authorize'),
    path(r'account/logout/', views.logout_view, name='logout_view'),
    path(r'account/check/', views.check, name='check'),
    path(r'account/create/', views.create_account, name='create_account'),
    
    path(r'links/delete_class_from_order/<int:ship_id>/', views.delete_class_from_order, name='delete_class_from_order'),
    path(r'links/change_imo/', views.change_imo, name='change_imo'),

    path('admin/', admin.site.urls),
]