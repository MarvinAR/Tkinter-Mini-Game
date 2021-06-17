class Player:

	def __init__(self, name='John'):
		self.name = name

	def current_location(self, pos_x, pos_y):
		self.location = (pos_x, pos_y)