from sys import argv
#получаем имя модуля для подключения, по-умолчанию vk_api
try:
	module_name = argv[1]
except IndexError:
	module_name = ''
module_name = module_name or 'vk_api'

try:
	exec('from ' + module_name + ' import Api')
except ImportError:
	raise FileNotFoundError('Module ' + argv[1] + ' do not found!')
#дополнительные модули
from time import sleep 
from core.logger import log_error as logger
from core.engine import get_response
from re import match
def main():  
	users = [] 
	with open('users.txt') as users_file:
		for line in users_file: 
			line = line.strip()
			if not(line) or line[0] == '#':
				continue
			user_arr = line.split(' ')
			if len(user_arr) != 2:
				continue
			user_id = user_arr[0]
			user_token = user_arr[1] 
			if not(match('^[0-9a-z]+$', user_id)):
				msg = user_id + ' is incorrect user_id'
				logger.log_error(msg)
				print(msg)
				continue
			#если все хорошо - добавляем в список с пользователями новый объект
			users.append(Api(user_id, user_token))	
	#запускаем цикл бота
	while True:
		#завершаем работу бота, если список с пользователями - пуст
		if not(len(users)): break
		for user in users:	
			#получаем текущие сообщения
			messages = user.get_messages();	
			for message in messages: 
				request = user.get_request(message['user_id'])
				if not(request): breakub
				""" получение ответа от движка
					№1 Уникальный идентификатор текущего аккаунта, может быть любым уникальным объектом
					№2 Уникальный идентификатор текущего пользователя, может быть любым уникальным объектом
					№3 Текст сообщения по которому будет определяться скрипт для запуска
					№4 Объект для передачи скрипту, может быть абсолютно любым объектом любой структуры

				"""
				response = get_response(user.id, message['user_id'], message['text'], request)
				user.send_response(message['user_id'], response) 
		#задержка
		sleep(2) 

#запуск основной функции
if __name__ == '__main__':
	main() 