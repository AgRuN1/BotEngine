class Iter:
	def __init__(self, elements, values, next_element):
		self.elements = elements
		self.next_element = next_element
		self.values = values

	def __iter__(self):
		return self

	def __next__(self):
		return self.next_element(self.values, self.elements)