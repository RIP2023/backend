from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import Order_Serializer,Class_of_Ship_Serializer,Order_for_Ship
from .models import Class_of_Ship,Order,Order_for_Ship,Custom_User
from rest_framework.decorators import api_view
import datetime



def get_user_id():
	return 1

def get_user_id_mod():
	return 1

# Методы УСЛУГ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
@api_view(['Get'])
def get_all_classes_of_ships(request, format=None):
    ships = Class_of_Ship.objects.all()
    if request.GET.get('name_filter'):
    	ships=Class_of_Ship.objects.filter(name__startswith = request.GET.get('name_filter'))
    serializer = Class_of_Ship_Serializer(ships, many=True)
    return Response(serializer.data)

@api_view(['Get'])
def get_one_class_of_ships(request,ship_id, 	format=None):
    ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
    if request.method == 'GET':
    	serializer = Class_of_Ship_Serializer(ship)
    	return Response(serializer.data)

@api_view(['Post'])
def post_add_class_of_ships(request, format=None):    
    serializer = Class_of_Ship_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])
def change_class_of_ship(request, ship_id, format=None):
    ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
    ships = Class_of_Ship.objects.get(ship_id=ship_id)
    serializer_ship = Class_of_Ship_Serializer(instance=ships, data=request.data,partial=True)
    if serializer_ship.is_valid():
        serializer_ship.save()
        return Response(serializer_ship.data)
    return Response(serializer_ship.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_class_of_ship(request, ship_id, format=None):    
    ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
    Class_of_Ship.objects.filter(ship_id=ship_id).update(status='F')
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['Post'])
def add_class_of_ship_to_order(request, ship_id, format=None):
	user_id = get_user_id()
	ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
	if Order.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
		pass
	else:
		Order.objects.create(creator=Custom_User.objects.get(id=user_id), status='Forming',start_date=datetime.datetime.now())
	Order_for_Ship.objects.create(ship_id = ship, order_id = Order.objects.get(creator=Custom_User.objects.get(id=user_id), status='Forming'))
	return Response(status=status.HTTP_204_NO_CONTENT)


# методы ЗАЯВОК !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

@api_view(['Get'])
def get_all_orders(request, format=None):
    orders = Order.objects.all().order_by('start_date','status')
    serializer = Order_Serializer(orders, many=True)
    return Response(serializer.data)

@api_view(['Get'])
def get_one_order(request, order_id,format = None):
	order = get_object_or_404(Order, order_id=order_id)
	if request.method == 'GET':
		serializer_order = Order_Serializer(order)
		comp_list = []
		for order_for_ship in Order_for_Ship.objects.filter(order_id=order_id):
			temp = Class_of_Ship_Serializer(order_for_ship.ship_id).data
			temp['imo_of_ship'] = order_for_ship.imo_of_ship
			comp_list.append(temp)
		cont = dict(serializer_order.data)
		cont['ships'] = comp_list
		return Response(cont)

@api_view(['Put'])
def approve_order(request,order_id, format=None):
	order = get_object_or_404(Order, order_id=order_id)
	user = Custom_User.objects.get(id=get_user_id_mod())
	if order.moderator != user:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if order.status != 'Active':
		return Response(status=status.HTTP_412_PRECONDITION_FAILED)
	Order.objects.filter(order_id=order_id).update(status='Finished',end_date = datetime.datetime.now())
	return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def decline_order(request,order_id, format=None):
	order = get_object_or_404(Order, order_id=order_id)
	user = Custom_User.objects.get(id=get_user_id_mod())
	if order.moderator != user:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if order.status != 'Active':
		return Response(status=status.HTTP_412_PRECONDITION_FAILED)
	Order.objects.filter(order_id=order_id).update(status='Declined',end_date=datetime.datetime.now())
	return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def form_order(request, format = None):
	user_id = get_user_id()
	if Order.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
		Order.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming').update(status = 'Active',moderator = Custom_User.objects.get(id=get_user_id_mod()),in_work=datetime.datetime.now())
		return Response(status=status.HTTP_204_NO_CONTENT)
	return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['Put'])
def delete_order(request, format = None):
	user_id = get_user_id()
	if Order.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
		Order.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming').update(status = 'Deleted')
		return Response(status=status.HTTP_204_NO_CONTENT)
	return Response(status=status.HTTP_404_NOT_FOUND)

# МЕТОДЫ ССЫЛОК М-М !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

@api_view(['Delete'])
def delete_class_from_order(request, ship_id, format=None):
	user_id = get_user_id()
	ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
	if Order.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
		record = get_object_or_404(Order_for_Ship,ship_id = ship,order_id = Order.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'))
		record.delete()
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)
	return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def change_imo(request, ship_id, format = None):
	user = get_object_or_404(Custom_User, id = get_user_id())
	if Order.objects.filter(creator=user, status='Forming'):
		order = Order.objects.get(creator=user, status='Forming')
		ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
		record = get_object_or_404(Order_for_Ship, ship_id=ship, order_id=order)
		Order_for_Ship.objects.filter(ship_id=ship, order_id=order).update(imo_of_ship = request.data['imo'])
		return Response(status=status.HTTP_204_NO_CONTENT)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)























