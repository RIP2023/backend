from django.shortcuts import render


class army_boat():
	def __init__(self,id,url_photo,name,type,rang):
		self.id = id
		self.url_photo = url_photo
		self.name = name
		self.type = type
		self.rang = rang

col_boat = []
col_boat.append(army_boat(1,'https://www.interfax.ru/ftproot/textphotos/2018/04/10/DDG700.jpg',"Ракетный эсминец","Эсминец",1))
col_boat.append(army_boat(2,'https://sdelanounas.ru/i/c/g/h/f_cGhvdG90YXNzNC5jZG52aWRlby5ydS93aWR0aC8xMDIwX2I5MjYxZmExL3Rhc3MvbTIvdXBsb2Fkcy9pLzIwMTkwMzA3LzQ5Nzc3MDIuanBnP19faWQ9MTE3OTMx.jpeg',"Атомная подводная лодка", "Подводная лодка",1))
col_boat.append(army_boat(3,'https://stat.mil.ru/images/military/gallery/2018/rgegaerg550.jpg',"Дизельная подводная лодка", "Подводная лодка",2))
col_boat.append(army_boat(4,'https://function.mil.ru/images/upload/2019/chf1_26112021_550%281%29.JPG',"Малый артиллерийский корабль", "Артиллерийский корабль",3))	
col_boat.append(army_boat(5,'https://v-pravda.ru/wp-content/uploads/2019/10/mak-volgodonsk.jpg',"Ракетный катер", "Катер",4))	


def ships(request):
	search_text = request.GET.get('filter')
	rang_1 = request.GET.get('rang_1')
	rang_2 = request.GET.get('rang_2')
	rang_3 = request.GET.get('rang_3')
	rang_4 = request.GET.get('rang_4')
	dict_rangs = {1:bool(rang_1),2:bool(rang_2),3:bool(rang_3),4:bool(rang_4)}
	if sum((bool(search_text),bool(rang_1),bool(rang_2),bool(rang_3),bool(rang_4))) == 0:
			return render(request,'user_all_boats.html',{'data':col_boat})
	search_res = []
	if sum((bool(rang_1),bool(rang_2),bool(rang_3),bool(rang_4))) == 0:
		for ship in col_boat:
			if ship.name.lower().startswith(search_text.lower()):
				search_res.append(ship)
	else:
		for ship in col_boat:
			if dict_rangs[ship.rang] and ship.name.lower().startswith(search_text.lower()):
				search_res.append(ship)


	return render(request,'user_all_boats.html',{'data':search_res})


def ship(request,ship_id):
	for ship in col_boat:
		if ship.id == ship_id:
			return render(request,'about_ship.html',{'boat':ship})

