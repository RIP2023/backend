from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
	is_manager = models.BooleanField(default = False)

	def __str__(self):
		return self.username

class Class_of_Ship(models.Model):
	ship_id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	photo_data = models.BinaryField(editable=True, blank = True, null = True)
	type = models.CharField(max_length = 20)
	rang = models.IntegerField()
	stuff = models.IntegerField()
	project = models.CharField(max_length = 20)
	description = models.TextField()
	status = models.CharField(max_length = 20)

class Order(models.Model):
	order_id = models.AutoField(primary_key = True)
	status = models.CharField(max_length = 20)
	start_date = models.DateTimeField(blank = True, null = True)
	in_work = models.DateTimeField(blank = True, null = True)
	end_date = models.DateTimeField(blank = True, null = True)
	moderator = models.ForeignKey(Custom_User, on_delete = models.CASCADE, related_name = 'moder',blank = True, null = True)
	creator = models.ForeignKey(Custom_User, on_delete = models.CASCADE, related_name = 'creator')

class Order_for_Ship(models.Model):
	ship_id = models.ForeignKey(Class_of_Ship, on_delete = models.CASCADE)
	order_id = models.ForeignKey(Order, on_delete = models.CASCADE)
	imo_of_ship = models.CharField(max_length = 20,blank = True, null = True)




	




