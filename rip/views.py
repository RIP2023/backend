from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from .models import Ship


def ships(request):
	search_text = request.GET.get('filter')
	rang_1 = request.GET.get('rang_1')
	rang_2 = request.GET.get('rang_2')
	rang_3 = request.GET.get('rang_3')
	rang_4 = request.GET.get('rang_4')
	arr_rangs = [rang_1,rang_2,rang_3,rang_4]
	for i in range(3,-1,-1):
		if not arr_rangs[i]:
			arr_rangs.pop(i)
		else:
			arr_rangs[i] = i+1
	if sum((bool(search_text),bool(rang_1),bool(rang_2),bool(rang_3),bool(rang_4))) == 0:
			return render(request,'user_all_boats.html',{'data':Ship.objects.filter(status='Добавлен'),'search_name':search_text})
	search_res = []
	if sum((bool(rang_1),bool(rang_2),bool(rang_3),bool(rang_4))) == 0:
		return render(request,'user_all_boats.html',{'data':Ship.objects.filter(name__startswith = search_text,status='Добавлен'),'search_name':search_text})
	else:
		return render(request,'user_all_boats.html',{'data':Ship.objects.filter(name__startswith = search_text,rang__in = arr_rangs,status='Добавлен'),'search_name':search_text})

def ship(request,ship_id):
	return render(request,'about_ship.html',{'boat':Ship.objects.get(ship_id=ship_id)})

def delete_ship(request,ship_id):
	with connection.cursor() as cursor:
		cursor.execute(f"UPDATE rip_ship SET status='Удалено' WHERE ship_id = {ship_id}")
	return redirect('http://127.0.0.1:8000/ships/')

