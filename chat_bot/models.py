from django.db import models

class ObjectsTypes(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length = 200)

class Objects(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length = 200)
	type_id = models.ForeignKey('ObjectsTypes', on_delete=models.CASCADE)
	
class ObjectsContent(models.Model):
	def __str__(self):
		if self.value_string:
			return self.value_string
		number_value = self.value_integer
		current_value = str(number_value)
		if current_value[-1] == '0':
			return current_value[0:-2]
		return current_value

	obj_id = models.ForeignKey('Objects', on_delete=models.CASCADE)
	field_id = models.ForeignKey('ObjectsFields', on_delete=models.CASCADE)
	value_string = models.CharField(max_length = 400, default = '')
	value_integer = models.FloatField(default = 0)

class ObjectsFields(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length = 200)
	type_id = models.ForeignKey('ObjectsTypes', on_delete=models.CASCADE)

class UserStep(models.Model):
	def __str__(self):
		return self.step

	step = models.CharField(max_length = 200)
	user_id = models.IntegerField(default = 0)
