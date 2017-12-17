class Middleware:
	response = None
	def __init__(self, accaunt_id, user_id, text, request):
		self.set_new(accaunt_id, user_id, text, request)

	def set_new(self, accaunt_id, user_id, text, request):
		self.accaunt_id = accaunt_id
		self.user_id = user_id
		self.text = text
		self.request = request

	def set_response(self, response):
		self.response = response

	
