class DataPoint:
	def __init__(self, data_type, data_name, data_value):
		self.data_type = data_type
		self.data_name = data_name
		self.data_value = data_value
	def __str__(self):
		return self.server_name + " -> " + self.data_type + " -> " + self.data_name + " -> " + str(self.data_value) + "\n"
	def __repr__(self):
		return self.server_name + " -> " + self.data_type + " -> " + self.data_name + " -> " + str(self.data_value) + "\n"
	def json(self):
		return "{\"serverName\": \"" + self.server_name + "\", \"dataType\": \"" + self.data_type + "\", \"dataName\": \"" + self.data_name + "\", \"dataValue\": \"" + str(self.data_value) + "\"}"
