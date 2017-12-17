from os import environ, path
import django

environ.setdefault("DJANGO_SETTINGS_MODULE", "config")
django.setup()

from chat_bot.models import Objects
from chat_bot.models import Objects_Types as Types
from chat_bot.models import Objects_Content as Content
from chat_bot.models import Objects_Fields as Fields
from chat_bot.models import User_Step as Steps
from core.Bot_Object import Object as Bot_Object
from core.helpers import check_name
from django.template.loader import get_template
from core.logger import log_error
from core.helpers import is_num

try:
	from Custom import Custom_Tools
except ImportError:
	class Custom_Tools: pass

class Tools(Custom_Tools):

	def __init__(self, path: str = '.') -> None:
		"""Указывает путь к исполняемому файлу"""
		self.path = path
		self.end = False
		self.save = True

	def get_type_id(self, type: str) -> int:
		"""Возвращает id типа по его имени"""
		current_types = Types.objects.filter(name = type)
		if len(current_types) == 0: 
			return False
		type_id = current_types[0].id
		return type_id

	def get_object(self, name: str='', type_name = '', type_id = 0, object_id = 0) -> 'Bot_Object':
		"""Возвращает объект по типу и имени или по уникальному id"""
		if object_id != 0 and is_num(object_id):
			current_objects = Objects.objects.filter(id = object_id)
			if len(current_objects) == 0:
				return False
			return Bot_Object(current_objects[0])
		if not(type_id):
			type_id = self.get_type_id(type_name)
		if not(self.check_type_id(type_id)):
			return False
		current_objects = Objects.objects.filter(type_id = type_id, name = name)
		if len(current_objects) == 0:
			return False
		return Bot_Object(current_objects[0])
	#пять методов, предназначенных для получения результатов выборки по одной из таблиц БД
	def find_objects(self, values={}) -> list:
		return Objects.objects.filter(**values)

	def find_types(self, values={}) -> list:
		return Types.objects.filter(**values)

	def find_contents(self, values={}) -> list:
		return Content.objects.filter(**values)

	def find_fields(self, values={}) -> list:
		return Fields.objects.filter(**values)

	def find_steps(self, values={}) -> list:
		return Steps.objects.filter(**values)

	def add_object(self, name: str, type_name = '', type_id = 0) -> int:
		"""Добавляет новый объект, указанного типа в бд"""
		if not(check_name(name)):
			return False
		if not(type_id):
			type_id = self.get_type_id(type_name)
		if self.check_type_id(type_id):
			current_objects = Objects.objects.filter(name = name, type_id = type_id)
			if len(current_objects) > 0:
				current_object = current_objects[0]
				return current_object.id
			new_object = Objects(name = name, type_id = type_id)
			new_object.save()
			return new_object.id
		else:
			return False

	def read_file(self, file: str, encoding = 'utf8') -> str:
		"""Читает файл, с выбранной кодировкой и возвращает содержимое"""
		try:
			f = open(path.join(self.path, file), 'r', encoding = encoding)
		except FileNotFoundError as e:
			msg = "Error: " + str(e)
			log_error(msg)
			print(msg)
			return False
		text = f.read()
		f.close()
		return text

	def get_template(self, tmp_name: str) -> 'Template':
		"""Возвращает объект шаблолна"""
		try:
			tmp = get_template(tmp_name)
		except TemplateDoesNotExist as e:
			msg = "Error: " + e
			log_error(msg)
			print(msg)
			return False
		return tmp

	def render_template(self, tmp_name: str, values: dict) -> str:
		"""Возвращает отрендеренный шаблон"""
		tmp = self.get_template(tmp_name)
		if not(tmp):
			return False
		try:
			return tmp.render(values)
		except TemplateSyntaxError as e:
			msg = "Error: " + str(e)
			log_error(msg)
			print(msg)
			return False

	def check_type_id(self, type_id: int) -> bool:
		"""Проверяет корректность идентификатора типа"""
		return len(Types.objects.filter(id = type_id)) != 0

	def set_end(self):
		"""Сообщает об окончании диалога диалога"""
		self.end = True

	def del_save(self):
		"""Отменяет запись сообщения в историю диалога"""
		self.save = False

	def create_response(self, response: '*') -> dict:
		"""Принимает объект любого типа, возвращает словарь ответа"""
		return {
			'response': response, 
			'end': self.end, 
			'save': self.save
		}

	
