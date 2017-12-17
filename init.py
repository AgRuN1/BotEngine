from os import path, mkdir, environ 
from re import match 
import django 

environ.setdefault("DJANGO_SETTINGS_MODULE", "config") 
django.setup()

#подключаем модели
from chat_bot.models import Objects_Types as Types
from chat_bot.models import Objects_Fields as Fields

from core.helpers import modify_text, check_name 
from core.logger import log_error
try:
	from config import OBJECTS_TYPES
except ImportError:
	OBJECTS_TYPES = {}

try:
	from config import BOT_MIDDLEWARES as middlewares
except ImportError:
	middlewares = []

def main():
	schema = open('schema.ini', 'r', encoding = 'utf8')
	mode = ''
	main_path = 'responses'
	path_count = -1
	for line in schema:
		line = line.strip()
		if not(line) or line[0] == '#': continue
		#если это определение типа, то сохраняем его
		if line[0] != '-': 
			mode = line.lower()
			continue
		command = line[1:]
		#проверка типа
		if mode == 'globals' or mode == 'scripts':
			# инициализируем каталог
			create_path(mode)
			create_file(path.join(mode, '__init__.py'))
			path_name = path.join(mode, command)
			path_name = create_path(path_name)
			init_work_path(path_name)
		elif mode == 'templates':
			create_path('tmp')
			create_file(path.join('tmp', command))
		elif mode == 'responses':
			create_path(mode)
			create_file(path.join(mode, '__init__.py'))
			#уровень вложенности
			current_path_count = 0
			while command[0] == '-':
				command = command[1:]
				current_path_count += 1
			#если вложенность отсутсвует - сбрасываем ее
			while current_path_count <= path_count:
				main_path = path.dirname(main_path)
				path_count -= 1
			path_count = current_path_count
			#проверяем наличие указателя на ссылку
			link_name = ''
			if match('.+\/link\/.+', command):
				link_name = path.basename(command)
				command = path.dirname(path.dirname(command))
			#добавляем необходимые файлы в каталог команды
			current_main_path = path.join(main_path, command)
			path_name = create_path(current_main_path)
			if link_name:
				create_file(path.join(path_name, 'link.txt'), link_name)
			else:
				init_work_path(path_name)
			main_path = path_name
		else:
			raise TypeError(mode + ' is a unknown mode')
	schema.close()
	create_path('log')
	create_path('scripts')
	create_path(path.join('scripts', 'error'))
	init_work_path(path.join('scripts', 'error'))
	
	#обновляем поля базы данных
	for type in OBJECTS_TYPES:
		if not(check_name(type)):
			msg = type + " is incorrect type name"
			log_error(msg)
			raise ValueError(msg)

		current_type = Types.objects.filter(name = type)
		if len(current_type) == 0:
			new_type = Types(name = type)
			new_type.save()
			type_id = new_type.id
		else:
			type_id = current_type[0].id
		for type_value in OBJECTS_TYPES[type]['values']:
			if not(check_name(type_value)):
				msg = type_value + " is incorrect value name"
				log_error(msg)
				raise ValueError(msg)
			current_value = Fields.objects.filter(name = type_value)
			if len(current_value) == 0:
				new_value = Fields(type_id = type_id, name = type_value)
				new_value.save()
		for added_field in Fields.objects.filter(type_id = type_id):
			if not(added_field.name in OBJECTS_TYPES[type]['values']):
				added_field.delete()
	for added_type in Types.objects.all():
		if added_type.name not in OBJECTS_TYPES:
			added_type.delete()

	if len(middlewares) != 0:
		create_path('middlewares')
		create_file(path.join('middlewares', '__init__.py'))
	for middleware in middlewares:
		mw_import = "from core.middleware import Middleware\n\n"
		mw_class = "class "+middleware+"(Middleware):\n\t"
		def_request = "def process_request(self, Tools, Logger): pass\n\t"
		def_response = "def process_response(self, Tools, Logger): pass\n\t"
		code = mw_import + mw_class + def_request + def_response
		create_file(path.join('middlewares', middleware+'.py'), code)
	
def init_work_path(path_name):
	create_file(path.join(path_name, '__init__.py'))
	code = 'def get_answer(request, Tools, Logger):\n\treturn Tools.create_response({})'
	create_file(path.join(path_name, "index.py"), code)

def create_path(dir_path):
	#преобразуем имя каталога, в случае необходимости
	command = modify_text(path.basename(dir_path))
	dir_path = path.join(path.dirname(dir_path), command)
	if not(path.exists(dir_path)):
		print("Create:", dir_path)
		mkdir(dir_path)
	return dir_path

def create_file(file_path, content = ''):
	if not(path.exists(file_path)):
		print('Create:', file_path)
		f = open(file_path, 'w', encoding = 'utf8')
		f.write(content)
		f.close()

if __name__ == '__main__': 
	main()