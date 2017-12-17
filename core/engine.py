from os import path, remove, listdir, environ
import django
#подключаем и запускаем необходимые модули
import core.logger as logger
from core.Tools import Tools
from core.helpers import modify_text

environ.setdefault("DJANGO_SETTINGS_MODULE", "config")
django.setup()

from chat_bot.models import User_Step as Step
from config import BOT_MIDDLEWARES

mw = None

def get_response(accaunt: str, user: str, text: str, message: '*') -> 'response':
	"""Возвращает ответ бота"""

	def error_handle():
		"""Обрабатывает ошибку"""
		if path.exists("scripts/error/index.py"):
			error_response = start_script("scripts/error")
			if not(error_response): 
				return False
			if 'response' not in error_response:
				return False
			return error_response['response']
		else:
			msg = "Didn't find error.py file"
			logger.log_error(msg)
			raise FileNotFoundError(msg)

	def start_script(path_to_dir) -> 'response':
		"""Запускает указанный скрипт"""
		tools = middlewares_tools
		request = message
		response = exec_script(path_to_dir, request)
		changed_data = False
		for middleware in middlewares:
			if changed_data:
				middleware.set_new(accaunt, user, text, request)
			middleware.set_response(response)
			try:
				middleware.process_response(tools, logger)
			except AttributeError:
				continue
			accaunt = middleware.accaunt_id
			user = middleware.user_id
			text = middleware.text
			request = middleware.request
			response = middleware.response
			changed_data = True
		return response

	middlewares = []
	middlewares_tools = Tools('middlewares')
	for middleware in BOT_MIDDLEWARES:
		middleware_path = path.join('middlewares', middleware + '.py')
		if not path.exists(middleware_path):
			msg = middleware + " middleware do not found"
			logger.log_error(msg)
			raise FileNotFoundError(msg)
		code = "from middlewares." + middleware + " import " + middleware + " as cmw; mw = cmw"
		exec(code, globals())
		current_middleware = mw(accaunt, user, text, message)
		middlewares.insert(0, current_middleware)
		try:
			current_middleware.process_request(middlewares_tools, logger)
		except AttributeError:
			continue
		if current_middleware.response != None:
			return current_middleware.response
		accaunt = current_middleware.accaunt_id
		user = current_middleware.user_id
		text = current_middleware.text
		message = current_middleware.request
	if not(text):
		return error_handle()
	if path.exists(path.join("globals", text)):
		global_response = start_script(path.join("globals", text))
		if not(global_response):
			return False
		if 'response' not in global_response:
			return False
		return global_response['response']
	users = Step.objects.filter(user_id=user)
	if not(len(users)):
		new_step = Step(user_id=user, step='')
		new_step.save()
		current_user = new_step
		if path.exists('responses/index.py'):
			return start_script('responses')
	else:
		current_user = users[0]
	text = text.replace(
		'.', ''
	).replace(
		"/", ''
	).replace(
		'\\', ''
	)
	text = modify_text(text)
	current_mode = current_user.step
	mode = path.join(current_mode, text)
	answer = False
	path_to_script = path.join("responses", mode)
	if path.exists(path.join(path_to_script, 'index.py')):
		answer = start_script(path_to_script)
	elif path.exists(path.join(path_to_script, "link.txt")):
		#получаем имя ссылки
		link_file = open(path.join(path_to_script, "link.txt"), 'r', encoding = 'utf8')
		link = link_file.read()
		link_file.close()
		if path.exists(path.join("scripts", link)):
			answer = start_script(path.join("scripts", link))
		else:
			msg = "Didn't find a message file"
			logger.log_error(msg)
			raise FileNotFoundError(msg)
	else:
		return error_handle()
	#если ответ отсутствует, возвращаем False
	if not(answer):
		return False

	if answer['end']:
		#удаляем информацию о пользователе, если диалог закончился
		Step.objects.filter(user_id = user)[0].delete()
	elif answer['save']:
		#изменяем шаг пользователя, на следующий
		user_step = Step.objects.filter(user_id = user)[0]
		user_step.step = mode
		user_step.save() 
	return answer['response']

	
g = None

def exec_script(path_dir: 'str', message: 'request') -> 'response':
	"""Передает запрос указанному скрипту"""
	path_to_script = path_dir.replace('/', '.').replace('\\', '.')
	global g
	code = "from "+path_to_script+".index import get_answer; g = get_answer"
	exec(code, globals())
	if not(callable(g)):
		msg = 'get_answer is not callable'
		logger.log_error(msg)
		raise AttributeError(msg)
	return g(message, Tools(path_dir), logger)