from os import environ
import django

environ.setdefault("DJANGO_SETTINGS_MODULE", "config")
django.setup()

from chat_bot.models import Objects
from chat_bot.models import ObjectsTypes as Types
from chat_bot.models import ObjectsContent as Content
from chat_bot.models import ObjectsFields as Fields
from core.helpers import is_num, check_name

def check_field_id(field_func: 'def') -> 'def':
	"""получение field_id по известным данным или False, если не удалось получить"""
	def wrapper(self, field_name: str='', field_id=0, **args) -> '*':
		if field_name:
			field_id = self.get_field_id(field_name)
		if not(field_id):
			return False
		return field_func(self, field_id, **args)
	return wrapper

class Object:
	def __init__(self, obj: 'Objects'):
		if not(isinstance(obj, Objects)):
			raise AttributeError('The given object is not a instance of vk_bot.models.Objects')
		self.object = obj

	def get_field_id(self, field_name: str) -> int:
		"""Получение field_id по имени"""
		current_fields= Fields.objects.filter(name=field_name, type_id=self.object.type_id)
		if len(current_fields) == 0:
			return False
		return current_fields[0].id

	@check_field_id
	def set_value(self, field_id: int, value='') -> int:
		"""Установка значения поля объекта"""
		current_values = Content.objects.filter(obj_id=self.object.id, field_id=field_id)
		if len(current_values) > 0:
			current_value = current_values[0]
			if is_num(value):
				current_values.value_integer = value
			else:
				current_value.value_string = value
			current_value.save()
			return current_value.id
		if is_num(value):
			new_value = Content(obj_id=self.object.id, field_id=field_id, value_integer=value)
		else:
			new_value = Content(obj_id=self.object.id, field_id=field_id, value_string=value)
		new_value.save()
		return new_value.id

	@check_field_id
	def get_value(self, field_id: int) -> 'str/int/float':
		"""получение значения свойства объекта"""
		current_values = Content.objects.filter(field_id=field_id, obj_id=self.object.id)
		if len(current_values) == 0:
			return False
		string_value = current_values[0].value_string
		if string_value:
			return string_value
		number_value = current_values[0].value_integer
		current_value = str(number_value)
		if current_value[-1] == '0':
			current_value = current_value[0:-2]
			return int(current_value)
		return float(current_value)

	@check_field_id
	def delete_value(self, field_id: int) -> bool:
		"""удаление значения свойства объекта"""
		current_values = Content.objects.filter(field_id=field_id, obj_id=self.object.id)
		if len(current_values) == 0:
			return False
		current_value = current_values[0]
		current_value.delete()
		return True

	def get_name(self) -> str:
		"""Получение имени текущего объекта"""
		return self.object.name

	def set_name(self, new_name: str) -> bool:
		"""Изменение имени текущего объекта"""
		if not(check_name(new_name)):
			return False
		self.object.name = new_name
		self.object.name.save()
		return True

	def get_values(self) -> dict:
		"""Получение словаря со все полями и их значениями текущего объекта"""
		contents = Content.objects.filter(obj_id=self.object.id)
		result = {}
		for content in contents:
			field = Fields.objects.get(id=content.field_id)
			if not(field): continue
			field_name = field.name
			field_value = self.get_value(field_id=field.id)
			result.setdefault(field_name, field_value)
		return result

	def get_type(self) -> str:
		"""Получение типа текущего объекта"""
		return Types.objects.filter(id=self.object.type_id)[0].name

	