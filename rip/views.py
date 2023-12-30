from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import Order_Serializer,Class_of_Ship_Serializer,Order_for_Ship,Custom_User_Serializer
from .models import Class_of_Ship,Order,Order_for_Ship,Custom_User,Order
from rest_framework.decorators import api_view
import datetime
from django.conf import settings
import redis
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import uuid
from drf_yasg.utils import swagger_auto_schema
import requests
import json
from django.contrib.auth import  logout


session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
ServerToken = 'abcde'
async_url = 'http://127.0.0.1:9000/'

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! МЕТОДЫ ПОЛЬЗОВАТЕЛЕЙ
@swagger_auto_schema(method='post',request_body=Custom_User_Serializer)
@api_view(['Post'])
def authorize(request):
    print(request.data)
    username = request.data["username"] # допустим передали username и password
    password = request.data["password"]
    user = authenticate(request, username=username, password=password)
    print(username)
    print(password)
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        
        response = Response({'session_id':random_key,'username':username,'is_moderator':Custom_User.objects.get(username=username).is_manager,"user_id":Custom_User.objects.get(username=username).id})
        print(response.data)
        response.set_cookie("session_id", random_key) # пусть ключем для куки будет session_id
        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")

@swagger_auto_schema(method='post',request_body=Custom_User_Serializer)
@api_view(['Post'])
def create_account(request):
	username = request.data["username"]
	email = request.data["email"]
	passwd = request.data["password"]
	try:
		Custom_User.objects.create_user(username = username, email = email, password = passwd)
		return HttpResponse("{'status': 'ok'}")
	except:
		return HttpResponse("{'status': 'error', 'error': 'wrong data'}")




@api_view(['Post'])
def check(request):
	print(request.headers)
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_401_UNAUTHORIZED)
	if ssid in session_storage:
		user = Custom_User.objects.get(username=session_storage.get(ssid).decode('utf-8'))
		data = {"is_moderator":user.is_manager,'username':user.username,'user_id':user.id}
		return Response(data, status=status.HTTP_200_OK)

	return Response(status=status.HTTP_403_FORBIDDEN)


@swagger_auto_schema(method='post')
@api_view(['Post'])
def logout_view(request):
	print(request.headers)
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_401_UNAUTHORIZED)
	try:
		Order.objects.get(status="Forming",creator=Custom_User.objects.get(username=session_storage.get(ssid).decode('utf-8'))).delete()
	except:
		pass
	session_storage.delete(ssid)
	response = HttpResponse(status=status.HTTP_200_OK)
	response.delete_cookie("session_id")
	return response

# Методы УСЛУГ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
@api_view(['Get'])
def get_all_classes_of_ships(request, format=None):
	try:
		ssid = request.headers["authorization"]
	except:
		ssid = ''
	print(ssid)
	if ssid and Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):
		user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
		print(user.username)
		if Order.objects.filter(creator=user, status='Forming'):
			print('AAAA')
			draft_id = Order.objects.get(creator=user, status='Forming').order_id
			print(draft_id)
			ships = Class_of_Ship.objects.filter(status="Добавлено")
			if request.GET.get('name_filter'):
				ships=Class_of_Ship.objects.filter(name__startswith = request.GET.get('name_filter').capitalize(),status="Добавлено")
			serializer = Class_of_Ship_Serializer(ships, many=True)
			d = dict()
			d['data'] = serializer.data
			d['draft_id'] = draft_id
			return Response(d)

	ships = Class_of_Ship.objects.filter(status="Добавлено")
	if request.GET.get('name_filter'):
		ships=Class_of_Ship.objects.filter(name__startswith = request.GET.get('name_filter').capitalize(),status="Добавлено")
	serializer = Class_of_Ship_Serializer(ships, many=True)
	d = dict()
	d['data'] = serializer.data
	d['draft_id'] = -1
	return Response(d)


@api_view(['Get'])
def get_one_class_of_ships(request,ship_id, 	format=None):
    ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
    if request.method == 'GET':
    	serializer = Class_of_Ship_Serializer(ship)
    	return Response(serializer.data)

@api_view(['Post'])
def post_add_class_of_ships(request, format=None): 
	print(request.COOKIES)
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	print(Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]))
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:   
		print(list(request.data.items()))
		d = {k:v for k,v in list(request.data.items())}
		d['rang'] = int(d['rang'])
		d['stuff'] = int(d['stuff'])
		d['status'] = 'Добавлено'
		try:
			d['photo_data'] = d['photo_data'][d['photo_data'].index('/9j'):]
		except:
			pass
		print(d['photo_data'])
		serializer = Class_of_Ship_Serializer(data=d)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['Put'])
def change_class_of_ship(request, ship_id, format=None):
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:   
		d = {}
		ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
		d["ship_id"] = ship_id
		d = {k:v for k,v in list(request.data.items())}
		d['rang'] = int(d['rang'])
		d['stuff'] = int(d['stuff'])
		try:
			d['photo_data'] = d['photo_data'][d['photo_data'].index('/9j'):]
		except:
			pass
		print
		serializer_ship = Class_of_Ship_Serializer(instance=ship, data=d,partial=True)
		if serializer_ship.is_valid():
			serializer_ship.save()
			return Response(serializer_ship.data)
		return Response(serializer_ship.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_class_of_ship(request, ship_id, format=None):
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:   
		ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
		Class_of_Ship.objects.filter(ship_id=ship_id).update(status='F')
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['Post'])
def add_class_of_ship_to_order(request, ship_id, format=None):
	print(request.data)
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]) is not None:
		usr = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
		print(usr.username)
		ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
		if Order.objects.filter(creator=usr, status='Forming'):
			pass
		else:
			Order.objects.create(creator=usr, status='Forming',start_date=datetime.datetime.now())
			print('A')
		Order_for_Ship.objects.create(ship_id = ship, order_id = Order.objects.get(creator=usr, status='Forming'))
		return Response(status=status.HTTP_204_NO_CONTENT)


# методы ЗАЯВОК !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

@api_view(['Get'])
def get_all_orders(request, format=None):
	# ничего - все
	# Только дата начала - выводим все с даты начала
	# Только дата конца - выводим все до даты конца
	# Две даты выводим между ними
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	print(request.GET)
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:
		beg = request.GET.get('begin_of_int')
		end = request.GET.get('end_of_int')
		try:
			status_param =  request.GET.get('status').split(',')
		except:
			status_param = ['Forming','Decline','Active','Aprove']
		if beg:
			orders = Order.objects.filter(in_work__gte=beg)
		if end:
			orders = Order.objects.filter(in_work__lte=end)
		if not (beg or end):
			orders = Order.objects.all()
		if beg and end:
			print("AA")
			orders = Order.objects.filter(in_work__range=(beg, end))
		if status_param:
			orders = orders.filter(status__in=status_param)
		serializer = Order_Serializer(orders, many=True)
		print(serializer.data)
		l = [i for i in serializer.data]
		
		for i in range(len(l)):
			l[i] = {k:v for k,v in l[i].items()}
			l[i]['count_of_imo'] = len(list(filter(lambda x: x.imo_of_ship is not None,Order_for_Ship.objects.filter(order_id=Order.objects.get(order_id=l[i]['order_id'])))))
		return Response(l)
	elif Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]) is not None:
		user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
		beg = request.GET.get('begin_of_int')
		end = request.GET.get('end_of_int')
		try:
			status_param =  request.GET.get('status').split(',')
		except:
			status_param = ['Forming','Decline','Active','Aprove']
		if beg:
			print(beg)
			orders = Order.objects.filter(in_work__gte=beg,creator=user)
			print(orders)
		if end:
			orders = Order.objects.filter(in_work__lte=end,creator=user)
		if beg and end:
			orders = Order.objects.filter(in_work__range=(beg, end),creator=user)
		if not (beg or end):
			orders = Order.objects.filter(creator=user)
		if status_param:
			orders = orders.filter(status__in=status_param)
		serializer = Order_Serializer(orders, many=True)
		l = [i for i in serializer.data]
		
		for i in range(len(l)):
			l[i] = {k:v for k,v in l[i].items()}
			l[i]['count_of_imo'] = len(list(filter(lambda x: x.imo_of_ship is not None,Order_for_Ship.objects.filter(order_id=Order.objects.get(order_id=l[i]['order_id'])))))
		print(l)
		return Response(l)
	else:
		return Response(status=status.HTTP_403_FORBIDDEN)

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
		print(cont['status'])
		return Response(cont)

@api_view(['Put'])
def approve_or_decline_order(request,order_id, format=None):
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:  
		status_ord = request.data['status']
		order = get_object_or_404(Order, order_id=order_id)
		user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
		if order.status != 'Active':
			return Response(status=status.HTTP_412_PRECONDITION_FAILED)
		Order.objects.filter(order_id=order_id).update(status=status_ord,moderator=user,end_date = datetime.datetime.now())
		return Response(status=status.HTTP_204_NO_CONTENT)
	else:
		return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['Put'])
def form_order(request, format = None):
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):  
		user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
		if Order.objects.filter(creator=user, status='Forming'):
			go_to_async(Order.objects.get(creator=user, status='Forming'))
			Order.objects.filter(creator=user, status='Forming').update(status = 'Active',in_work=datetime.datetime.now())
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['Put'])
def delete_order(request, format = None):
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):  
		user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
		if Order.objects.filter(creator=user, status='Forming'):
			Order.objects.filter(creator=user, status='Forming').update(status = 'Deleted')
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(status=status.HTTP_404_NOT_FOUND)

# МЕТОДЫ ССЫЛОК М-М !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

@api_view(['Delete'])
def delete_class_from_order(request, ship_id, format=None):
	try:
		ssid = request.headers["authorization"]
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):  
		user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
		ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
		print(Order.objects.filter(creator=user, status='Forming'))
		if Order.objects.filter(creator=user, status='Forming'):
			record = Order_for_Ship.objects.filter(ship_id = ship,order_id = Order.objects.get(creator=user, status='Forming'))[0]
			record.delete()
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def change_imo(request, format = None):
	try:
		token = request.data['Server-Token']
	except:
		return Response(status=status.HTTP_403_FORBIDDEN)
	if token == ServerToken:  
		order_id = request.data['order_id']
		ship_id = request.data['ship_id']
		if Order.objects.get(order_id=order_id):
			order = Order.objects.get(order_id=order_id)
			ship = get_object_or_404(Class_of_Ship, ship_id=ship_id)
			record = get_object_or_404(Order_for_Ship, ship_id=ship, order_id=order)
			Order_for_Ship.objects.filter(ship_id=ship, order_id=order, imo = '').update(imo_of_ship = request.data['imo'])
			return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

def go_to_async(order):
	order_id = order.order_id
	payload = {'order_id':order_id}
	for ship in Order_for_Ship.objects.filter(order_id=order):
		payload['ship_id'] = ship.ship_id.ship_id
		try:
			requests.put(url=async_url,data=json.dumps(payload),timeout=3)
		except:
			pass




