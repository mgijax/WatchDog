import json,httplib

class RestClient:

	def __init__(self, config):
		self.restserver = config['collector_server_name']
		self.restport = config['collector_server_port']
		self.baseurl = "/rest"

	def senddatapoint(self, json_string):
		endpoint = "/datapoint"
		connection = httplib.HTTPConnection(self.restserver, self.restport)
		connection.connect()
		connection.request('POST', self.baseurl + endpoint, json.dumps(json.loads(json_string)), {"Content-Type": "application/json"})
		result = connection.getresponse().read()
		return result
