from django.db import models

class Objects_Types(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length = 200)

class Objects(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length = 200)
	type_id = models.IntegerField(default = 0)

class Objects_Content(models.Model):
	def __str__(self):
		if self.value_string:
			return self.value_string
		number_value = self.value_integer
		current_value = str(number_value)
		if current_value[-1] == '0':
			current_value = current_value[0:-2]
			return current_value
		return current_value

	obj_id = models.IntegerField(default = 0)
	field_id = models.IntegerField(default = 0)
	value_string = models.CharField(max_length = 400, default = '')
	value_integer = models.FloatField(default = 0)

class Objects_Fields(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length = 200)
	type_id = models.IntegerField(default = 0)

class User_Step(models.Model):
	def __str__(self):
		return self.step

	step = models.CharField(max_length = 200)
	user_id = models.IntegerField(default = 0)
