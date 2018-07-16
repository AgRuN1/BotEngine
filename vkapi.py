import vk
import core.logger as logger
from core.Iter import Iter
from time import sleep
from config import LAST_DATE

class Api:
	def __init__(self, user_id, user_token):
		self.id = user_id;
		session = vk.Session(user_token)
		self.vk_api = vk.API(session, v='5.52')

	def next_dialog(self, values: dict, dialogs: list) -> list:
		if values['offset'] ==  values['count'] and values['offset']:
			raise StopIteration
		new_dialogs = self.get_dialog(offset = values['offset'])
		if len(new_dialogs) == 1: 
			raise StopIteration
		values['offset'] += len(new_dialogs['items'])
		values['count'] = new_dialogs['count']
		return new_dialogs['items']

	def get_dialog(self, offset = 0) -> list:
		try:
			dialog = self.vk_api.messages.getDialogs(offset = offset)
		except BaseException as e:
			msg = 'Error: ' + self.id + " : " + str(e)
			logger.log_error(msg)
			print(msg)
			raise StopIteration
		return dialog

	def get_request(self, user_id: int) -> dict:
		try:
			history = self.vk_api.messages.getHistory(user_id = user_id)
			history = history['items']
		except BaseException as e:
			msg = "Error: " + self.id + " : " + str(e)
			logger.log_error(msg)
			print(msg)
			return False
		current_message = history[0]
		request = {}
		request['text'] = current_message['body']
		request['user_id'] = current_message['user_id']
		if 'attachments' in current_message:
			request['attachments'] = current_message['attachments']
		else:
			request['attachments'] = []
		request['msg_id'] = current_message['id']
		return request

	def get_messages(self) -> 'generator':
		values = {
			'offset': 0,
			'count': 0
		}

		dialogs_iterator = Iter([], values, self.next_dialog)
		end_cycle = False
		for dialogs_arr in dialogs_iterator:
			for current_dialog in dialogs_arr:
				current_dialog = current_dialog['message']
				if current_dialog['date'] < LAST_DATE:
					end_cycle = True
					break
				if current_dialog['out'] or current_dialog['read_state']:
					continue
				dialog = {
					'user_id': current_dialog['user_id'],
					'text': current_dialog['body']
				}
				yield dialog
			if end_cycle: break
			


	def send_response(self, user_id: int, response: dict) -> bool:
		print(response)
		if not(response):
			return False
		if 'attachments' in response:
			attachments = ','.join(response['attachments'])
		else:
			attachments = ''
		if 'text' in response:
			text = response['text']
		else:
			text = ''
		if not(text) and not(attachments):
			return False
		reply = False
		try:
			reply = self.vk_api.messages.send(user_id = user_id, message = text, attachment = attachments)
		except BaseException as e:
			msg = "Send : " + str(e)
			logger.log_error(msg)
			print(msg)
			return False
		return bool(reply)