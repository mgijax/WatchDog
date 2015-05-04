class Statistic:
	def __init__(self, server_name, data_type, data_name, data_value):
		self.server_name = server_name
		self.data_type = data_type
		self.data_name = data_name
		self.data_value = data_value
	def __str__(self):
		return self.server_name + " -> " + self.data_type + " -> " + self.data_name + " -> " + str(self.data_value) + "\n"
	def __repr__(self):
		return self.server_name + " -> " + self.data_type + " -> " + self.data_name + " -> " + str(self.data_value) + "\n"
