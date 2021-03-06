# This class is used to hold the data that will be sent
# to the monitoring server for collection. Several methods
# are defined in order to represent the data in different ways.
class DataPoint:
	def __init__(self, data_type, data_name, data_prop, data_value):
		self.data_type = data_type
		self.data_name = data_name
		self.data_prop = data_prop
		self.data_value = data_value
	def __str__(self):
		return "[" + self.server_name + " -> " + self.data_type + " -> " + self.data_name + " -> " + self.data_prop + " -> " + str(self.data_value) + "]"
	def __repr__(self):
		return "[" + self.server_name + " -> " + self.data_type + " -> " + self.data_name + " -> " + self.data_prop + " -> " + str(self.data_value) + "]"
	def json(self):
		return "{\"serverName\": \"" + self.server_name + "\", \"dataType\": \"" + self.data_type + "\", \"dataName\": \"" + self.data_name + "\", \"dataProperty\": \"" + self.data_prop + "\", \"dataValue\": \"" + str(self.data_value) + "\"}"
